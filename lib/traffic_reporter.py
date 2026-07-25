"""2plot.ai satellite traffic reporter — feeds the owner-only /traffic hub.

Implements the satellite side of the network's analytics contract (see
2plotai's docs/network/satellite-analytics.md): each hour this process
POSTs a signed rollup of today's (and yesterday's, to close out the day
across midnight/deploys) traffic to
``https://2plot.ai/api/satellite/traffic``, HMAC-signed with the shared
``CROSS_APP_WEBHOOK_SECRET`` (the same scheme as the ad-network client and
every other cross-app webhook in the network). Re-POSTing the same
(app, date) overwrites on the hub, so reporting today's numbers every hour
just firms them up as the day progresses.

Hits are persisted to an append-only JSONL ledger (one small dict per
pageview) and every rollup is rebuilt from that ledger — so a restart or
deploy mid-day does NOT reset the counts and the next hourly POST cannot
overwrite the hub's row with a smaller number. Point
``TRAFFIC_ANALYTICS_FILE`` at a mounted disk to survive deploys too.

Wiring (run.py, after the app is built):
    from lib.traffic_reporter import register_traffic_reporting
    register_traffic_reporting(app)

Env:
    CROSS_APP_WEBHOOK_SECRET — shared HMAC secret. Unset → reporting is a
                                no-op (hits still ledger, nothing POSTed).
    SATELLITE_APP_KEY        — this app's 2plot network-directory key
                                (default "email"). NOT chained to AD_APP_ID:
                                ad identities are not directory keys.
    TRAFFIC_ANALYTICS_FILE   — ledger path (default ./satellite_traffic.jsonl;
                                point at a mounted disk in production).
    TRAFFIC_REPORT_URL       — override the hub endpoint (tests / staging).
"""
from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import statistics
import threading
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

APP_KEY = os.environ.get("SATELLITE_APP_KEY") or "email"

TRAFFIC_REPORT_URL = os.environ.get(
    "TRAFFIC_REPORT_URL", "https://2plot.ai/api/satellite/traffic"
)


def _ledger_path() -> Path:
    return Path(os.environ.get("TRAFFIC_ANALYTICS_FILE")
                or "satellite_traffic.jsonl")


_REPORT_INTERVAL_S = 3600
# short first delay: free-tier containers can be idle-evicted ~15 min after
# waking — report early so every wake window lands at least one rollup (the
# hub accumulates across resets, so partial windows still add up).
_FIRST_REPORT_DELAY_S = 90
_SESSION_GAP_S = 1800  # 30 minutes — same rule the hub uses, per the contract
_HTTP_TIMEOUT_S = 10
_RETENTION_DAYS = 3

_SKIP_PATH_MARKERS = (
    "_dash-component-suites", "_dash-layout", "_dash-dependencies",
    "_dash-update-component", "_reload-hash", "/assets/", "/healthz",
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".map",
)

_lock = threading.Lock()
_session_started = False


def _utc_day(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%d")


def _today_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _should_skip(path: str) -> bool:
    if not path or not path.startswith("/") or path.startswith("//"):
        return True
    return any(marker in path for marker in _SKIP_PATH_MARKERS)


def _client_key(ip: str, user_agent: str) -> str:
    return hashlib.sha256(f"{ip}|{user_agent}".encode()).hexdigest()[:16]


def record_hit(path: str, headers: dict, remote_addr: str) -> None:
    """Ledger one request. Fail-silent — a tracking bug must never break a
    page view. Row: {"t": epoch, "p": path, "v": client key, "b": 0|1,
    "c": country?} — tiny on purpose, rebuilt into a rollup on demand."""
    try:
        if _should_skip(path):
            return

        lc_headers = {k.lower(): v for k, v in (headers or {}).items()}
        user_agent = lc_headers.get("user-agent", "") or ""

        # Behind Cloudflare, CF-IPCountry/CF-Connecting-IP are the accurate,
        # free source — no need to geolocate. Falls back to the raw remote
        # address when the app isn't behind Cloudflare (e.g. local dev).
        ip = lc_headers.get("cf-connecting-ip") or remote_addr or "unknown"
        country = (lc_headers.get("cf-ipcountry") or "").upper()

        from dash_improve_my_llms.bot_detection import is_any_bot

        row = {"t": round(time.time(), 2), "p": path[:160],
               "v": _client_key(ip, user_agent),
               "b": 1 if is_any_bot(user_agent) else 0}
        if country and country not in ("XX", "T1"):
            row["c"] = country
        line = json.dumps(row, separators=(",", ":")) + "\n"
        with _lock:
            with open(_ledger_path(), "a", encoding="utf-8") as f:
                f.write(line)
    except Exception:
        logger.debug("traffic_reporter.record_hit failed", exc_info=True)


def _load_rows() -> list[dict]:
    try:
        with _lock, open(_ledger_path(), encoding="utf-8") as f:
            rows = []
            for line in f:
                try:
                    rows.append(json.loads(line))
                except Exception:
                    continue  # torn line from a crash mid-write
            return rows
    except FileNotFoundError:
        return []
    except Exception:
        logger.debug("traffic_reporter ledger read failed", exc_info=True)
        return []


def _prune() -> None:
    """Rewrite the ledger keeping only the retention window."""
    cutoff = time.time() - _RETENTION_DAYS * 86400
    try:
        rows = [r for r in _load_rows() if (r.get("t") or 0) >= cutoff]
        with _lock:
            tmp = _ledger_path().with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                for r in rows:
                    f.write(json.dumps(r, separators=(",", ":")) + "\n")
            os.replace(tmp, _ledger_path())
    except Exception:
        logger.debug("traffic_reporter prune failed", exc_info=True)


def _sessions_for(hits: list) -> list:
    """Split one client's sorted hit timestamps into sessions on 30-min gaps."""
    hits = sorted(hits)
    sessions = [[hits[0]]]
    for t in hits[1:]:
        if t - sessions[-1][-1] > _SESSION_GAP_S:
            sessions.append([t])
        else:
            sessions[-1].append(t)
    return sessions


def build_rollup(day: str | None = None) -> dict | None:
    """Build the payload for one UTC day (default: today) from the ledger.

    Returns None for a day with zero recorded hits — better to send
    nothing than to overwrite a real hub row with zeros after the ledger
    was lost (fresh deploy without a mounted disk).
    """
    day = day or _today_key()
    rows = [r for r in _load_rows() if _utc_day(r.get("t") or 0) == day]
    if not rows:
        return None

    humans = [r for r in rows if not r.get("b")]
    clients: dict[str, list] = {}
    pages: Counter = Counter()
    countries: Counter = Counter()
    for r in humans:
        clients.setdefault(r["v"], []).append(r["t"])
        pages[r["p"]] += 1
        if r.get("c"):
            countries[r["c"]] += 1

    all_sessions = [s for hits in clients.values() for s in _sessions_for(hits)]
    multi_page_spans = [s[-1] - s[0] for s in all_sessions if len(s) > 1]

    payload = {
        "app": APP_KEY,
        "date": day,
        "human_hits": len(humans),
        "bot_hits": len(rows) - len(humans),
    }
    if clients:
        payload["visitors"] = len(clients)
    if all_sessions:
        payload["sessions"] = len(all_sessions)
    if multi_page_spans:
        payload["median_session_s"] = round(statistics.median(multi_page_spans), 1)
    if pages:
        payload["pages"] = [{"path": p, "hits": n}
                            for p, n in pages.most_common(20)]
    if countries:
        payload["countries"] = dict(countries.most_common(20))
    return payload


def _send(payload: dict) -> bool:
    secret = os.environ.get("CROSS_APP_WEBHOOK_SECRET")
    if not secret:
        logger.debug("traffic_reporter: CROSS_APP_WEBHOOK_SECRET unset, skipping report")
        return False
    body = json.dumps(payload).encode()
    ts = str(int(time.time()))
    sig = hmac.new(secret.encode(), f"{ts}.".encode() + body, hashlib.sha256).hexdigest()
    try:
        resp = requests.post(
            TRAFFIC_REPORT_URL,
            data=body,
            headers={
                "Content-Type": "application/json",
                "X-AI-Canvas-Timestamp": ts,
                "X-AI-Canvas-Signature": sig,
            },
            timeout=_HTTP_TIMEOUT_S,
        )
        if resp.status_code != 200:
            logger.warning("traffic report rejected (%s): %s", resp.status_code, resp.text[:200])
            return False
        return True
    except Exception as e:
        logger.warning("traffic report failed: %s", e)
        return False


def _report_pass() -> None:
    """Report today AND yesterday — the yesterday re-POST closes out the
    day across midnight and heals deploy gaps (hub overwrites per date)."""
    today = _today_key()
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    for day in (yesterday, today):
        payload = build_rollup(day)
        if payload is not None:
            _send(payload)


def _report_loop():
    time.sleep(_FIRST_REPORT_DELAY_S)
    while True:
        try:
            _report_pass()
            _prune()
        except Exception:
            logger.exception("traffic_reporter loop crashed")
        time.sleep(_REPORT_INTERVAL_S)


def register_traffic_reporting(app) -> None:
    """Hook Flask's before_request and start the hourly report thread.

    Safe to call once per process; a second call is a no-op (avoids a
    duplicate reporting thread under a dev-server reload).
    """
    global _session_started
    if _session_started:
        return
    _session_started = True

    from flask import request as flask_request

    @app.server.before_request
    def _track_traffic():
        record_hit(flask_request.path, dict(flask_request.headers), flask_request.remote_addr)

    if not os.environ.get("CROSS_APP_WEBHOOK_SECRET"):
        logger.info("traffic_reporter: CROSS_APP_WEBHOOK_SECRET not set — "
                    "local hits are ledgered but nothing is reported to 2plot.ai")

    threading.Thread(target=_report_loop, daemon=True).start()
