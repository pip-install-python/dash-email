#!/usr/bin/env python
"""Headless smoke test for dash-email.

Boots ``run.py`` in-process and drives it through Flask's **test client** —
real request/response handling, no socket bind — then reports one line per
check. This is the same harness ``scripts/compat_matrix.py`` runs against each
Dash version, so what passes here is what the matrix measures.

What it checks
--------------
1. **Import** — ``run.py`` imports and constructs the Dash app.
2. **Component surface** — all 15 ``dash_email`` classes exist, the JS bundle
   is registered in ``_js_dist`` and present on disk, and a representative
   email tree builds and survives Dash's JSON encoder. This is the *package*
   leg; it does not depend on the docs site at all.
3. **Registration** — every ``docs/<slug>/<slug>.md`` became a page, with no
   duplicate paths.
4. **Layout render** — every page's layout is serialised with Dash's own JSON
   encoder. This is where a broken example.py, a bad prop, or a missing
   component actually surfaces.
5. **HTTP** — ``GET`` each page path plus ``/_dash-layout``,
   ``/_dash-dependencies``, ``/healthz``, ``/llms.txt``, ``/robots.txt`` and
   ``/sitemap.xml``.
6. **Clientside JS** — every inline clientside callback is syntax-checked with
   node. Dash ships those strings to the browser verbatim, so a syntax error
   is completely silent server-side and the callback simply never runs.
7. **Assets** — ``assets/*.js`` parsed individually *and* concatenated, because
   Dash serves them as separate classic ``<script>`` tags sharing one global
   lexical scope.

Usage
-----
    python scripts/smoke_test.py                 # human-readable table
    python scripts/smoke_test.py --json out.json # machine-readable
    python scripts/smoke_test.py --quiet         # only failures

Exit code is 0 when every check passed, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

# Flask's test client is the only backend whose in-process client needs no
# extra dependency, and the page/layout checks are backend-independent.
os.environ.setdefault("DASH_BACKEND", "flask")
# Never let a smoke run beacon traffic at the live 2plot.ai hub, and keep the
# ad client from adding a network timeout to every page.
os.environ.pop("CROSS_APP_WEBHOOK_SECRET", None)
os.environ.setdefault("AD_SERVER_URL", "http://127.0.0.1:1")  # unreachable → slot hides
# The traffic ledger is append-only; a smoke run must not grow the repo's copy.
os.environ.setdefault(
    "TRAFFIC_ANALYTICS_FILE",
    str(Path(tempfile.gettempdir()) / "dash-email-smoke-traffic.jsonl"),
)

# The public component surface. Adding a component means adding it here — that
# is the point: the wheel must never silently lose one.
COMPONENTS = [
    "Email", "EmailHead", "EmailPreview", "EmailBody",
    "EmailContainer", "EmailSection", "EmailRow", "EmailColumn",
    "EmailHeading", "EmailText", "EmailButton", "EmailLink",
    "EmailImage", "EmailDivider", "EmailFont",
]


class Results:
    def __init__(self) -> None:
        self.checks: list[dict] = []

    def add(self, group: str, name: str, ok: bool, detail: str = "") -> None:
        self.checks.append({"group": group, "name": name, "ok": ok, "detail": detail})

    @property
    def failures(self) -> list[dict]:
        return [c for c in self.checks if not c["ok"]]

    def summary(self) -> dict:
        return {
            "total": len(self.checks),
            "passed": len(self.checks) - len(self.failures),
            "failed": len(self.failures),
        }


def _check_package(res: Results) -> None:
    """The component library on its own — no docs site involved.

    This is deliberately the first group. If `dash_email` itself is broken the
    docs-site failures downstream are noise, and this is also the only group
    that means anything to someone who ran `pip install dash-email`.
    """
    try:
        import dash_email as de
    except Exception:
        res.add("package", "dash_email imports", False, traceback.format_exc(limit=6))
        return
    res.add("package", "dash_email imports", True, f"v{getattr(de, '__version__', '?')}")

    missing = [c for c in COMPONENTS if not hasattr(de, c)]
    res.add("package", f"all {len(COMPONENTS)} components exported", not missing,
            "complete" if not missing else "MISSING: " + ", ".join(missing))

    extra = sorted(set(de.__all__) - set(COMPONENTS))
    if extra:
        res.add("package", "no undeclared exports", False,
                "not in this script's COMPONENTS list: " + ", ".join(extra))

    dist = getattr(de, "_js_dist", [])
    res.add("package", "_js_dist registered", bool(dist), f"{len(dist)} entries")
    pkg_dir = Path(de.__file__).parent
    for entry in dist:
        bundle = pkg_dir / entry["relative_package_path"]
        res.add("package", f"bundle {entry['relative_package_path']}", bundle.exists(),
                f"{bundle.stat().st_size // 1024} KB" if bundle.exists()
                else "MISSING — run npm run build")

    # Build the shape a real template has: nesting, table layout, every prop
    # kind, and run it through Dash's encoder — the same path app.layout takes.
    try:
        from dash._utils import to_json

        tree = de.Email(lang="en", children=[
            de.EmailHead([de.EmailFont(fontFamily="Inter",
                                       fallbackFontFamily="Helvetica")]),
            de.EmailPreview("Preview text"),
            de.EmailBody(style={"backgroundColor": "#f6f9fc"}, children=[
                de.EmailContainer([
                    de.EmailSection([
                        de.EmailHeading("Welcome", as_="h1"),
                        de.EmailText("Body copy."),
                        de.EmailImage(src="https://example.com/a.png", alt="a",
                                      width=120, height=40),
                        de.EmailDivider(),
                        de.EmailRow([
                            de.EmailColumn(style={"width": "70%"},
                                           children=[de.EmailText("Product")]),
                            de.EmailColumn(style={"width": "30%"},
                                           children=[de.EmailText("$99.00")]),
                        ]),
                        de.EmailButton("Go", href="https://example.com"),
                        de.EmailLink("or read more", href="https://example.com"),
                    ]),
                ]),
            ]),
        ])
        payload = to_json(tree)
        res.add("package", "full template serialises", True, f"{len(payload)} bytes JSON")
    except Exception as exc:  # noqa: BLE001
        res.add("package", "full template serialises", False,
                f"{type(exc).__name__}: {exc}")


def _import_app(res: Results):
    """Import run.py and hand back (module, dash)."""
    t0 = time.time()
    try:
        import run  # noqa: F401  (side effects are the point)
        import dash

        res.add("import", "run.py imports", True, f"{time.time() - t0:.1f}s")
        return run, dash
    except Exception:
        res.add("import", "run.py imports", False, traceback.format_exc(limit=8))
        return None, None


def _check_registration(res: Results, dash_mod) -> None:
    registry = dash_mod.page_registry
    md_files = sorted(Path("docs").glob("**/*.md"))
    res.add("pages", "markdown files discovered", bool(md_files), f"{len(md_files)} files")

    paths = [entry["path"] for entry in registry.values()]
    dupes = {p for p in paths if paths.count(p) > 1}
    res.add("pages", "no duplicate page paths", not dupes, ", ".join(sorted(dupes)) or "clean")

    # Every markdown file should have produced a route.
    missing = []
    for md in md_files:
        try:
            import frontmatter

            meta, _ = frontmatter.parse(md.read_text())
            endpoint = meta.get("endpoint")
            if endpoint and endpoint not in paths:
                missing.append(f"{md} → {endpoint}")
        except Exception as exc:  # noqa: BLE001
            missing.append(f"{md} (frontmatter unreadable: {exc})")
    res.add("pages", "every .md registered a route", not missing,
            "; ".join(missing) or "all present")


def _render_layouts(res: Results, dash_mod) -> None:
    """Invoke and serialise every page layout — where broken examples surface."""
    from dash._utils import to_json

    for entry in dash_mod.page_registry.values():
        path, name = entry["path"], entry["name"]
        try:
            layout = entry["layout"]
            if callable(layout):
                layout = layout()
            to_json(layout)  # Dash's own encoder — catches invalid components
            res.add("layout", f"{path}", True, name)
        except Exception as exc:  # noqa: BLE001
            res.add("layout", f"{path}", False, f"{type(exc).__name__}: {exc}")


def _http_checks(res: Results, run_mod, dash_mod) -> None:
    server = run_mod.app.server
    try:
        client = server.test_client()
    except Exception as exc:  # noqa: BLE001
        res.add("http", "test client available", False, str(exc))
        return
    res.add("http", "test client available", True, type(server).__name__)

    def get(url: str, group: str, expect=(200,), label: str | None = None):
        try:
            resp = client.get(url)
            code = resp.status_code
            ok = code in expect
            res.add(group, label or url, ok, f"HTTP {code}")
            return resp
        except Exception as exc:  # noqa: BLE001
            res.add(group, label or url, False, f"{type(exc).__name__}: {exc}")
            return None

    # Dash plumbing first — if these fail nothing else matters.
    get("/_dash-layout", "http")
    get("/_dash-dependencies", "http")

    # Network + SEO endpoints.
    get("/healthz", "endpoints")
    get("/llms.txt", "endpoints")
    get("/robots.txt", "endpoints")
    get("/sitemap.xml", "endpoints")

    # Every page path. A Dash SPA returns the same index HTML for all of them,
    # so a non-200 means routing or the index template broke.
    for entry in dash_mod.page_registry.values():
        get(entry["path"], "routes")


def _check_callbacks(res: Results, dash_mod, run_mod) -> None:
    try:
        app = run_mod.app
        cb_count = len(app.callback_map)
        res.add("callbacks", "callbacks registered", cb_count > 0, f"{cb_count} callbacks")
    except Exception as exc:  # noqa: BLE001
        res.add("callbacks", "callbacks registered", False, str(exc))


def _check_clientside_js(res: Results, run_mod) -> None:
    """Syntax-check every inline clientside callback with node.

    Python-side tests cannot catch a malformed clientside callback: Dash ships
    the string to the browser verbatim, so a syntax error is silent
    server-side and the callback simply never runs. dash-email has two of them
    — the ad-network click beacon and the llms-copy button — and both would
    fail exactly this way.
    """
    scripts = getattr(run_mod.app, "_inline_scripts", [])
    if not scripts:
        res.add("clientside", "inline scripts collected", False, "none found")
        return
    res.add("clientside", "inline scripts collected", True, f"{len(scripts)} scripts")

    if not shutil.which("node"):
        res.add("clientside", "javascript parses", True, "SKIPPED — node not installed")
        return

    bad: list[str] = []
    for i, src in enumerate(scripts):
        proc = subprocess.run(
            ["node", "--check", "-"], input=src,
            capture_output=True, text=True, timeout=20,
        )
        if proc.returncode:
            first = next((ln for ln in proc.stderr.splitlines() if ln.strip()), "")
            bad.append(f"script[{i}]: {first[:120]}")

    res.add(
        "clientside", "javascript parses", not bad,
        "all valid" if not bad else f"{len(bad)} invalid — " + "; ".join(bad[:3]),
    )


def _check_asset_js(res: Results) -> None:
    """Syntax-check assets/*.js individually AND concatenated.

    The concatenated pass is the one that matters. Dash serves everything in
    `assets/` as separate classic <script> tags, which share ONE global lexical
    scope — so a top-level `const log` in two files is a SyntaxError in the
    second, and every handler in it silently never registers. Checking files
    one at a time cannot see that: each is valid alone.
    """
    assets = sorted(Path("assets").glob("*.js"))
    if not assets:
        return
    if not shutil.which("node"):
        res.add("assets", "javascript parses", True, "SKIPPED — node not installed")
        return

    bad = []
    for f in assets:
        proc = subprocess.run(["node", "--check", str(f)],
                              capture_output=True, text=True, timeout=20)
        if proc.returncode:
            first = next((ln for ln in proc.stderr.splitlines() if "Error" in ln), "")
            bad.append(f"{f.name}: {first[:80]}")
    res.add("assets", f"each of {len(assets)} files parses", not bad,
            "all valid" if not bad else "; ".join(bad[:3]))

    combined = "\n".join(f.read_text() for f in assets)
    proc = subprocess.run(["node", "--check", "-"], input=combined,
                          capture_output=True, text=True, timeout=30)
    ok = proc.returncode == 0
    detail = "no global collisions"
    if not ok:
        detail = next((ln for ln in proc.stderr.splitlines() if "Error" in ln),
                      "see node output")[:120]
    res.add("assets", "no collisions in shared global scope", ok, detail)


def _check_seo(res: Results, run_mod, dash_mod) -> None:
    """The head-tag and network contract, enforced so it cannot silently revert.

    Rewritten for dash-improve-my-llms 2.3.3, which changed who owns what.
    Under 2.0.0 this app hand-rolled its own canonical/title injection; 2.3.3
    prerenders both, but **only for requests it identifies as bots**. So the
    contract is asserted on the crawler path — which is the path these tags
    exist for — and the browser path is only checked for the one thing that
    would be actively harmful there, a duplicated canonical.

    Every check corresponds to a bug this site actually had, or to one the
    2.3.3 upgrade could reintroduce:

    * `<title>` was `Dash` on all 11 routes (Dash resolves the per-page title
      only in the browser).
    * `<link rel=canonical>` was hard-coded to the site root, so every page
      declared itself a duplicate of one other page.
    * Two canonical tags appeared the moment 2.3.3 started prerendering while
      the local 2.0-era shim was still installed.
    * robots.txt said `Disallow: /` for OAI-SearchBot under a heading reading
      "Allow AI Search and Citation Bots" (a 2.0.0 bug fixed in 2.3.2).
    * The peer directory listed two subdomains that do not resolve.
    """
    from html.parser import HTMLParser

    class Head(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.metas: list[dict] = []
            self.canonicals: list[dict] = []
            self.title = ""
            self._in_title = False

        def handle_starttag(self, tag, attrs):
            d = dict(attrs)
            if tag == "meta":
                self.metas.append(d)
            elif tag == "link" and d.get("rel") == "canonical":
                self.canonicals.append(d)
            elif tag == "title":
                self._in_title = True

        def handle_data(self, data):
            if self._in_title:
                self.title += data

        def handle_endtag(self, tag):
            if tag == "title":
                self._in_title = False

    try:
        client = run_mod.app.server.test_client()
    except Exception as exc:  # noqa: BLE001
        res.add("seo", "test client available", False, str(exc))
        return

    from lib.constants import DOCS_BASE_URL

    origin = DOCS_BASE_URL.rstrip("/")
    # /admin/* is excluded from every crawl-surface sweep here on purpose: the
    # control board fails CLOSED to anonymous renders (its machine surfaces
    # are mark_hidden, it is deliberately absent from the sitemap, and its
    # crawler body carries no title/canonical/charset to check). Sweeping it
    # like a docs route flags exactly the behavior the gate exists for —
    # tests/test_control_board.py owns that page's assertions. Same exclusion
    # as tests/conftest.py's `pages` fixture.
    pages = [entry for entry in dash_mod.page_registry.values()
             if not entry["path"].startswith("/admin/")]

    # A UA the package's bot detector recognises. The prerendered document is
    # what search engines and unfurlers actually index.
    CRAWLER = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    BROWSER = {"User-Agent": "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/120 Safari/537.36"}

    # Tags that must never appear twice in one document.
    NEVER_DUPLICATE = [
        "description", "og:title", "og:description", "og:type", "og:image",
        "og:url", "twitter:card", "twitter:title", "twitter:description",
        "twitter:url", "twitter:image", "viewport", "keywords", "author",
        "og:site_name",
    ]

    def parse(path, headers):
        html = client.get(path, headers=headers).get_data(as_text=True)
        head_html = html.split("</head>")[0]
        h = Head()
        h.feed(head_html)
        return h, head_html

    bad_title, bad_canonical, dupes, late_charset, browser_dupe_canon = [], [], [], [], []
    for entry in pages:
        path = entry["path"]
        try:
            head, head_html = parse(path, CRAWLER)
        except Exception as exc:  # noqa: BLE001
            bad_title.append(f"{path} ({exc})")
            continue

        # 1. A real, page-specific title. 2.3.3 sets it from the page NAME,
        #    not the registry `title`, so assert non-generic rather than equal.
        #
        #    The HOME PAGE is exempt from the "not app.title" half, and that is
        #    the network standard rather than a loosened check. `run.py` calls
        #    `register_page_metadata(path="/", name=SITE_BRAND)` — the one
        #    registration that makes the /llms.txt H1 and the llms viewer's
        #    brand chip say what this site is — and 2.3.4 prerenders the title
        #    from the same name. So `/` legitimately serves the brand, which
        #    `Dash(title=)` also carries. Requiring them to differ would force
        #    the site to publish two names for itself, which is the exact drift
        #    tests/test_site_identity.py exists to prevent.
        #
        #    Every other route stays strict: a page that falls back to the
        #    app-wide title is the real failure, and it is still caught.
        title = head.title.strip()
        generic = ("Dash",) if path == "/" else ("Dash", run_mod.app.title)
        if not title or title in generic:
            bad_title.append(f"{path} → {title!r}")

        # 2. Exactly one canonical, pointing at this page on the real origin.
        want = origin + path
        if len(head.canonicals) != 1:
            bad_canonical.append(f"{path}: {len(head.canonicals)} canonical tags")
        elif head.canonicals[0].get("href") != want:
            bad_canonical.append(f"{path} → {head.canonicals[0].get('href')}")

        # 3. No tag emitted twice on the crawler path.
        seen: dict[str, int] = {}
        for m in head.metas:
            key = m.get("name") or m.get("property")
            if key:
                seen[key] = seen.get(key, 0) + 1
        for key in NEVER_DUPLICATE:
            if seen.get(key, 0) > 1:
                dupes.append(f"{path}: {key} x{seen[key]}")

        # 4. Encoding declaration inside the spec's 1024-byte window.
        lowered = head_html.lower()
        if "<meta charset=" in lowered:
            i = lowered.index("<meta charset=")
            end = head_html.index(">", i) + 1
            if end > 1024:
                late_charset.append(f"{path}: byte {end}")
        else:
            late_charset.append(f"{path}: no charset declaration")

        # 5. The browser path must never carry TWO canonicals. Zero is fine
        #    there (the package prerenders for bots only); two is what the
        #    retired 2.0-era shim produced once 2.3.3 started injecting.
        bhead, _ = parse(path, BROWSER)
        if len(bhead.canonicals) > 1:
            browser_dupe_canon.append(f"{path}: {len(bhead.canonicals)}")

    res.add("seo", f"per-page <title> on all {len(pages)} routes", not bad_title,
            "all page-specific" if not bad_title else "; ".join(bad_title[:3]))
    res.add("seo", "one correct canonical per route", not bad_canonical,
            f"→ {origin}/…" if not bad_canonical else "; ".join(bad_canonical[:3]))
    res.add("seo", "no duplicate head tags (crawler)", not dupes,
            "clean" if not dupes else "; ".join(dupes[:4]))
    res.add("seo", "no duplicate canonical (browser)", not browser_dupe_canon,
            "clean" if not browser_dupe_canon else "; ".join(browser_dupe_canon[:3]))
    res.add("seo", "charset within first 1024 bytes", not late_charset,
            "conforming" if not late_charset else "; ".join(late_charset[:3]))

    # 6. The template's origin token must have been substituted at startup.
    from lib.constants import ORIGIN_PLACEHOLDER

    index_html = client.get("/").get_data(as_text=True)
    res.add("seo", "origin token substituted", ORIGIN_PLACEHOLDER not in index_html,
            origin if ORIGIN_PLACEHOLDER not in index_html
            else f"{ORIGIN_PLACEHOLDER} still in served HTML")

    # ---------------------------------------------------------------- robots
    robots = client.get("/robots.txt").get_data(as_text=True)
    groups: dict[str, list[str]] = {}
    agent = None
    for line in robots.splitlines():
        line = line.strip()
        if line.lower().startswith("user-agent:"):
            agent = line.split(":", 1)[1].strip()
            groups.setdefault(agent, [])
        elif agent and (line.lower().startswith("allow:")
                        or line.lower().startswith("disallow:")):
            groups[agent].append(line)

    def disallowed(a):
        return any(r.lower().startswith("disallow: /") for r in groups.get(a, []))

    contradictory = [a for a, rules in groups.items()
                     if any(r.lower().startswith("allow:") for r in rules)
                     and any(r.lower().startswith("disallow: /") for r in rules)]
    res.add("seo", "no self-contradicting robots group", not contradictory,
            "consistent" if not contradictory else ", ".join(contradictory))

    dup_groups = [a for a in groups if robots.count(f"User-agent: {a}\n") > 1]
    res.add("seo", "no duplicate robots user-agent group", not dup_groups,
            "one group per agent" if not dup_groups
            else "a leftover custom_rules workaround? " + ", ".join(dup_groups[:3]))

    # The 2.3.3 taxonomy is per-vendor, not per-company: the TRAINING crawlers
    # are blocked while the user-triggered and search fetchers stay allowed.
    # ClaudeBot belongs in the first list — it is Anthropic's training crawler,
    # not its search one. Getting that backwards is what this guards.
    AI_SEARCH = ["OAI-SearchBot", "ChatGPT-User", "Claude-User",
                 "Claude-SearchBot", "PerplexityBot"]
    blocked = [a for a in AI_SEARCH if disallowed(a)]
    res.add("seo", "AI-search crawlers allowed", not blocked,
            f"{len(AI_SEARCH)} allowed" if not blocked else "BLOCKED: " + ", ".join(blocked))

    # block_ai_training=False silently emits no training bucket at all, which
    # reads as "balanced" and is actually "training allowed". This is also the
    # >=2.3.3 fingerprint: 2.0.0 could not produce it.
    AI_TRAINING = ["GPTBot", "ClaudeBot", "CCBot"]
    unblocked = [a for a in AI_TRAINING if not disallowed(a)]
    res.add("seo", "AI-training crawlers blocked", not unblocked,
            f"{len(AI_TRAINING)} disallowed" if not unblocked
            else "NOT blocked: " + ", ".join(unblocked))

    # --------------------------------------------------------------- network
    llms = client.get("/llms.txt").get_data(as_text=True)
    res.add("seo", "llms.txt publishes the network directory", "## Network" in llms,
            "## Network present" if "## Network" in llms
            else "network_directory.apply() not wired?")

    # Peers that are known not to resolve — a dead entry is one an agent
    # follows once before distrusting the whole list. pannellum.2plot.dev and
    # emojimart.2plot.dev lived here while they were NXDOMAIN (measured
    # 2026-07-31); both shipped live in the gate wave's batch 1 (2026-08-21/22)
    # and the canonical directory rightly lists them again. The check stays
    # armed so the next retirement has somewhere to land.
    DEAD_PEERS = []
    listed_dead = [d for d in DEAD_PEERS if d in llms]
    res.add("seo", "no known-dead peer advertised", not listed_dead,
            "directory clean" if not listed_dead
            else "NXDOMAIN as of 2026-07-31: " + ", ".join(listed_dead))

    res.add("seo", "app does not list itself as a peer",
            llms.count(f"]({origin})") == 0,
            "self excluded from PEERS")

    # Directive leakage into agent-facing markdown — fixed in 2.3.3, and the
    # markdown is what an agent reads instead of the page.
    leaked = []
    for entry in pages:
        body = client.get(entry["path"].rstrip("/") + "/llms.txt").get_data(as_text=True)
        if re.search(r"^\.\. \w+::", body, re.M):
            leaked.append(entry["path"])
    res.add("seo", "no directive leak in page llms.txt", not leaked,
            f"{len(pages)} pages clean" if not leaked else ", ".join(leaked[:3]))

    # ------------------------------------------------------------- sitemap
    sitemap = client.get("/sitemap.xml").get_data(as_text=True)
    absent = [p["path"] for p in pages if f"<loc>{origin}{p['path']}</loc>" not in sitemap]
    res.add("seo", "sitemap covers every route", not absent,
            f"{len(pages)} URLs" if not absent else "missing: " + ", ".join(absent[:3]))


def _check_bundle_js(res: Results) -> None:
    """Parse the shipped component bundle itself.

    A truncated or half-written `dash_email.min.js` still imports fine from
    Python — `_js_dist` only records a path — and then every component on
    every page renders as nothing in the browser.
    """
    bundle = PROJECT_ROOT / "dash_email" / "dash_email.min.js"
    if not bundle.exists() or not shutil.which("node"):
        return
    proc = subprocess.run(["node", "--check", str(bundle)],
                          capture_output=True, text=True, timeout=30)
    ok = proc.returncode == 0
    res.add("assets", "component bundle parses",
            ok, "valid" if ok else proc.stderr.splitlines()[0][:120])


def run_all() -> Results:
    res = Results()
    _check_package(res)
    run_mod, dash_mod = _import_app(res)
    if run_mod is None:
        return res
    _check_registration(res, dash_mod)
    _render_layouts(res, dash_mod)
    _http_checks(res, run_mod, dash_mod)
    _check_callbacks(res, dash_mod, run_mod)
    _check_seo(res, run_mod, dash_mod)
    _check_clientside_js(res, run_mod)
    _check_asset_js(res)
    _check_bundle_js(res)
    return res


def report(res: Results, quiet: bool = False) -> None:
    import dash

    width = 78
    print()
    print("=" * width)
    print(f" dash-email smoke test · Dash {dash.__version__} · Python {sys.version.split()[0]}")
    print("=" * width)

    current = None
    for c in res.checks:
        if quiet and c["ok"]:
            continue
        if c["group"] != current:
            current = c["group"]
            print(f"\n[{current}]")
        mark = "PASS" if c["ok"] else "FAIL"
        detail = c["detail"].replace("\n", "\n        ") if c["detail"] else ""
        print(f"  {mark}  {c['name']:<38} {detail}")

    s = res.summary()
    print()
    print("-" * width)
    print(f" {s['passed']}/{s['total']} checks passed"
          + (f" · {s['failed']} FAILED" if s["failed"] else ""))
    print("-" * width)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", metavar="PATH", help="write machine-readable results here")
    ap.add_argument("--quiet", action="store_true", help="print only failures")
    args = ap.parse_args()

    res = run_all()
    report(res, quiet=args.quiet)

    if args.json:
        import dash

        payload = {
            "dash_version": getattr(dash, "__version__", "unknown"),
            "python": sys.version.split()[0],
            "summary": res.summary(),
            "checks": res.checks,
        }
        Path(args.json).write_text(json.dumps(payload, indent=2))
        print(f"\nWrote {args.json}")

    return 0 if not res.failures else 1


if __name__ == "__main__":
    sys.exit(main())
