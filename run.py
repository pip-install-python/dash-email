"""
Dash Email — documentation site + AI-powered email builder.

Serves the component documentation (markdown-driven, docs/**/*.md) alongside
the /email-builder application. Run locally:

    python run.py                 # http://127.0.0.1:8054

Production (Render/Docker):

    gunicorn run:server -b 0.0.0.0:8054
"""
import os
import sys

import dash
from dash import Dash
from dotenv import load_dotenv

# MUST come before the first-party imports below, and this is not style.
# Several modules read os.environ at *import* time — lib/constants.py
# (DASH_EMAIL_BASE_URL), lib/ad_client.py (AD_SERVER_URL, AD_APP_ID) and
# lib/analytics_tracker.py (TRAFFIC_ANALYTICS_FILE). Loading the .env after
# importing them means every one of those silently falls back to its default
# no matter what the file says. Render passes real process env vars so
# production was unaffected, which is exactly why this stayed invisible.
load_dotenv()

# THE FORK POINT — claim this app's network identity before any hub-facing
# module imports. Every module that names this app (satellite_reporter,
# ad_client, hub_client, bulletin) carries its own fallback default, and
# after a template sync those defaults can DISAGREE: the byte-copied
# reporter says "boilerplate" while this fork's other modules say "email",
# so an unset SATELLITE_APP_KEY files this app's traffic under the
# TEMPLATE's hub row (found live on pannellum, 2026-08-21). setdefault: a
# real env value (Render dashboard, the .env loaded above) always wins;
# this line only closes the unset gap. FORKS CHANGE THIS ONE STRING.
os.environ.setdefault("SATELLITE_APP_KEY", "email")

from components.appshell import create_appshell  # noqa: E402
from lib import bulletin, network_directory  # noqa: E402
from lib.analytics_tracker import tracker  # noqa: E402
from lib.constants import (  # noqa: E402
    APP_VERSION,
    DOCS_BASE_URL,
    OG_IMAGE_ALT,
    OG_IMAGE_HEIGHT,
    OG_IMAGE_URL,
    OG_IMAGE_WIDTH,
    ORIGIN_PLACEHOLDER,
    PUBLISHER,
    SAME_AS,
    SITE_BRAND,
    SITE_DESCRIPTION,
    require_owned_base_url,
)

from dash_improve_my_llms import (  # noqa: E402
    __version__ as LLMS_PKG_VERSION,
    add_llms_routes,
    LLMSConfig,
    RobotsConfig,
    on_document_read,
    register_page_metadata,
)

print(
    f"[dash-email] Starting Dash {dash.__version__} "
    f"(dash-improve-my-llms {LLMS_PKG_VERSION})"
)

# ----------------------------------------------------------------------------
# Dependency floor — enforced, not advised.
#
# An IDE run configuration pointing at another project's virtualenv starts
# this app quite happily against whatever versions that environment holds,
# serves visibly older behaviour, and a warning scrolls past above a wall of
# page-loading logs. So a version below the floor stops the boot and says
# what to do. Set ALLOW_STALE_DEPS=1 to downgrade to a warning when
# deliberately testing an older release.
# ----------------------------------------------------------------------------

# The version requirements.txt pins. 2.8.0 is the ledger floor (item 12,
# the ledger row): ONE classifier — `classify()` is the registry
# robots.txt is rendered from, and lib/analytics_tracker delegates to it
# instead of carrying a fourth UA list that filed ClaudeBot (Anthropic's
# TRAINING crawler) as "search"; the READ EVENT — `on_document_read` hands
# the app one row per corpus document served (tier, verdict, bytes,
# verified vendor), which the tracker keeps as the ledger's `reads` table
# next to `visits`; and verified vendor identity (`verified` is `n/a`
# where the operator publishes no ranges — Anthropic does not, so
# ClaudeBot is always n/a here). Underneath, 2.7.1 is the round-3 fleet
# floor: 2.7.0 dedups the prerender H1 (every page served TWO h1s to
# crawlers — the injected header plus the doc body's own markdown H1) and
# the home footer's doubled /llms.txt link, and hardens the idempotency
# probe so a page that MENTIONS the marker no longer loses its prerender
# (the marker-in-comment trap — the very defect that blanked THIS host's
# every prerender until the gate-wave pass found it in
# templates/index.html). 2.7.1 adds the llms.txt v2 discovery relations
# (rel=alternate/describedby on both lanes + Link headers), the
# Accept: text/plain ramp, and the representation digest — the surfaces
# the network's agent lane composes over. Further underneath, 2.6.1 keeps
# the universal prerender VISIBLE (below it the block carries a literal
# `hidden` attribute, so every visibility-respecting consumer reads
# "Loading..." instead of the page's prose — the outside-audit finding of
# 2026-08-22), and 2.6.0 keeps sitemap <lastmod> honored instead of
# swallowed into **kwargs. The same number lives in requirements.txt,
# .github/workflows/ci.yml (twice), tests/test_pages.py and
# scripts/check_release.py — grep the number, don't move one.
LLMS_PKG_FLOOR = (2, 8, 0)

ALLOW_STALE_DEPS = os.environ.get("ALLOW_STALE_DEPS", "0") == "1"


def _version(text: str) -> tuple:
    """("2.6.1rc0") -> (2, 6, 1). Trailing rc/dev segments are dropped."""
    parts = []
    for chunk in text.split(".")[:3]:
        digits = ""
        for char in chunk:
            if not char.isdigit():
                break
            digits += char
        if not digits:
            break
        parts.append(int(digits))
    return tuple(parts)


if LLMS_PKG_FLOOR > _version(LLMS_PKG_VERSION):
    _floor_msg = (
        f"dash-improve-my-llms {LLMS_PKG_VERSION} is below the "
        f"{'.'.join(str(n) for n in LLMS_PKG_FLOOR)} floor in "
        "requirements.txt. Below 2.8.0 there is no `classify()` and no "
        "`on_document_read`: the tracker cannot delegate bot classification "
        "and no read row is ever kept, so the ledger's `reads` table and "
        "rollup v4's vendors[] are empty. Below 2.7.1 the llms.txt v2 "
        "discovery relations (rel=alternate/describedby + Link headers), "
        "the text/plain Accept ramp, and the representation digest are "
        "missing. Below 2.7.0 every page serves a DUPLICATE H1 to crawlers "
        "(the injected prerender header plus the doc body's own), the home "
        "footer doubles its /llms.txt link, and a page that merely "
        "MENTIONS the prerender marker loses its prerender entirely (the "
        "marker-in-comment trap). Below 2.6.1 the universal prerender ships "
        "`hidden`; below 2.6.0 sitemap lastmod dates are silently swallowed; "
        "below 2.5.1 configure_seo does not exist and the crawler document "
        "carries no site identity at all.\n"
        f"    running from: {sys.executable}\n"
        "    fix: point your run configuration at this project's own .venv, "
        "or reinstall with `pip install -r requirements.txt`.\n"
        "    (set ALLOW_STALE_DEPS=1 to start anyway)"
    )
    if not ALLOW_STALE_DEPS:
        raise RuntimeError("\n[dash-email] " + _floor_msg)
    print("[dash-email] WARNING: " + _floor_msg)

# Imported after the floor on purpose: on a pre-2.5.0 package this name does
# not exist, and the floor's diagnosis above beats a bare ImportError. The
# fallback exists only for ALLOW_STALE_DEPS=1 — the floor is fatal otherwise.
try:
    from dash_improve_my_llms import configure_seo  # noqa: E402
except ImportError:  # pragma: no cover — ALLOW_STALE_DEPS with an old package

    def configure_seo(**_kwargs) -> None:
        print(
            "[dash-email] WARNING: configure_seo unavailable (pre-2.5.0 "
            "package) — crawler identity tags and root icons not emitted."
        )


# Refuses to boot in production if the canonical origin is a platform-generated
# hostname. `*.onrender.com` keeps resolving after the custom domain is
# attached, so a base URL pointing there splits link equity across two hosts
# and nothing about the running site looks wrong.
require_owned_base_url()

# ----------------------------------------------------------------------------
# Clerk satellite auth. MUST run BEFORE Dash(...) — register_clerk_auth
# installs @dash.hooks callbacks that fire during app construction, so calling
# it afterwards silently does nothing. Fully optional: a no-op with no CLERK_*
# keys, which is the default. See lib/auth.py.
# ----------------------------------------------------------------------------
from lib import auth as _auth  # noqa: E402

CLERK_ENABLED = _auth.register()

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,
    update_title=None,
    # The template's __CANONICAL_ORIGIN__ tokens become DOCS_BASE_URL here, so
    # the canonical origin, the JSON-LD urls and the llms.txt links all come
    # from lib/constants.py. A static file cannot import that module, and two
    # hand-maintained copies of an origin is exactly how half a site ends up
    # pointing at one hostname and half at another. __APP_VERSION__ is the
    # same idea for the JSON-LD `version` field: scripts/check_release.py
    # already pins APP_VERSION to package.json, so substituting it here means
    # the published version can never lag a release.
    index_string=open('templates/index.html').read().replace(
        ORIGIN_PLACEHOLDER, DOCS_BASE_URL
    ).replace("__APP_VERSION__", APP_VERSION),
    # Dash interpolates the title placeholder with `self.title` and never
    # resolves the per-page title server-side. From 2.3.3 the package's
    # prerender layer rewrites <title> per route for us, so this is the
    # fallback for paths outside the page registry — where "Dash" would
    # otherwise be served.
    #
    # It is also `resolve_site_title`'s second candidate (2.3.4), which is why
    # it carries SITE_BRAND verbatim rather than a prose sentence: one string,
    # every surface. tests/test_site_identity.py pins it.
    title=SITE_BRAND,
)

# dash-clerk-auth splits its setup either side of Dash(...): sessions, the
# /api/auth/* routes and per-request identity are wired here. No-op when off.
_auth.configure_app(app)

# ----------------------------------------------------------------------------
# Trust the proxy's forwarded scheme. Immediately after the server object
# exists and before anything can serve a request. Dash builds `twitter:url`
# from `request.url` for every page, and behind Cloudflare -> Render the last
# hop is plain HTTP, so the site would advertise `http://email.2plot.dev/` to
# every social scraper while `og:url` (which templates/index.html hard-codes)
# looked correct. Scrapers do not run JavaScript, so the client-side canonical
# sync in the template cannot reach this. See lib/proxy.py.
# ----------------------------------------------------------------------------
from lib import proxy as _proxy  # noqa: E402

PROXY_FIX_APPLIED = _proxy.apply(app, "flask")
print(
    "[dash-email] forwarded-scheme trust: "
    + ("on" if PROXY_FIX_APPLIED else "OFF — request.url will report the "
       "scheme of the last proxy hop, and social cards will advertise it")
)

# ============================================================================
# AI/LLM & SEO configuration (dash-improve-my-llms)
# ============================================================================

app._base_url = DOCS_BASE_URL

# Cross-host directory: <link rel="related"> tags, a `## Network` section in
# /llms.txt, and followed links in the prerendered body. Search engines follow
# cross-host links weakly and agents do not follow them at all, so without this
# an agent landing here sees one library and nothing saying the rest exist —
# sitemap.xml cannot help, being scoped to its own origin by design.
#
# The definition lives in lib/network_directory.py (copied verbatim from the
# boilerplate) and `peers_for()` drops this app from its own peer list.
# Must run before add_llms_routes so the routes are built with it in place.
network_directory.apply(DOCS_BASE_URL)

# Crawler posture — THE WALL IS RETIRED (sync item 15, 1.6.37, owner
# decision 2026-08-29, ported here 2026-08-30). This host blocked the
# AI-training crawlers (GPTBot, ClaudeBot, CCBot, …) through the 2.7.1
# floor round: robots.txt said Disallow and the package's middleware
# answered 403 on the browser document and /healthz, while the corpus
# (/llms.txt and the tiers) stayed open — a wall that decided by vendor
# class what nobody could account for. Sync item 12 changed that: every
# corpus read is now a ledger row (tier, vendor, verified, bytes), and
# the hub can reconcile it against the wire. A read that is recorded and
# priceable does not need a wall; it needs a policy. So training
# crawlers are ALLOWED by default, same as search fetchers and
# traditional bots, and the per-vendor knob is the tool from here on —
# block or meter ONE vendor by name when its ledger rows justify it,
# never the whole class:
#
#     vendor_policy={"bytespider": "block", "gptbot": "meter"}
#
# (2.3.3's per-vendor buckets still matter: they are what makes a
# per-vendor line mean the vendor it names.) This fork has no
# DIVERGENCES.md posture fence to declare `ai_bots` 403-by-design in —
# see DIVERGENCES.md entry 6 (item 9 not adopted here); this repo has
# no lockdown reason to keep the wall, so the flip applies unconditionally.
app._robots_config = RobotsConfig(
    block_ai_training=False,      # training crawlers allowed; the ledger records every read
    allow_ai_search=True,         # Allow Claude-User/-SearchBot, ChatGPT-User, ...
    allow_traditional=True,       # Allow Googlebot, Bingbot, etc.
    crawl_delay=10,
    disallowed_paths=[],
)

# `name` here is NOT a nav label — dash.register_page in pages/home.py owns
# that, and it says "Home". This is what dash-improve-my-llms 2.3.4's
# `resolve_site_title` reads first, so it is the /llms.txt H1 and the llms
# viewer's brand chip: the two surfaces an agent uses to learn what this site
# is.
#
# `resolve_site_title` SKIPS generic candidates ("Home", "Index", "Dash"), so
# passing the page's display name here would silently fall through to
# `app.title` instead of erroring. Nothing would look broken.
#
# schema_type matches the static JSON-LD in templates/index.html:
# SoftwareSourceCode, not SoftwareApplication — this describes an open-source
# library you import, not a hosted app you sign up for. NO lastmod here, on
# purpose: the home page is a living index and declares no date rather than
# an invented one; docs pages stamp real dates in their frontmatter.
register_page_metadata(
    path="/",
    name=SITE_BRAND,
    description=SITE_DESCRIPTION,
    schema_type="SoftwareSourceCode",
)

register_page_metadata(
    path="/email-builder",
    name="Email Builder",
    description=(
        "AI-powered email template builder: generate dash-email layouts with "
        "Google Gemini, preview them live, export Python code, and send via "
        "Resend."
    ),
    llms_doc=(
        "# Email Builder\n\n"
        "AI-powered email template builder built on dash-email components.\n\n"
        "- Describe the email you want (18 email types across marketing, "
        "transactional, and professional categories) and Google Gemini "
        "generates a dash-email layout.\n"
        "- Preview the rendered email live, tweak it, and export ready-to-use "
        "Python code.\n"
        "- Send single or batch (up to 100 recipients) test emails via the "
        "Resend API, with optional scheduling.\n\n"
        "Requires GOOGLE_API_KEY (generation) and RESEND_API_KEY (sending) "
        "environment variables.\n"
    ),
)

# ============================================================================
# Site identity for the CRAWLER document (dash-improve-my-llms 2.5.0).
# Until 2.5.0 the generated crawler HTML carried the page's content signals
# and none of its identity: browsers got the icon links, og:image and a
# twitter card from templates/index.html while Googlebot got zero of any of
# them — so search showed the generic globe. One declaration covers every
# crawler surface, and it also claims /favicon.ico (Google's fallback), which
# Dash's page catch-all was answering with the app shell. Content may differ
# between the crawler document and the browser document; identity may not.
# ============================================================================
configure_seo(
    icons=[
        # Same paths templates/index.html links, so the two heads agree.
        # The .ico href is the assets/favicon/ copy (byte-identical to the
        # root one Dash's {%favicon%} placeholder finds) so this list is
        # SET-equal to what 2.6.0's autodiscovery finds —
        # tests/test_seo_icons.py pins that agreement.
        "/assets/favicon/favicon.ico",
        {"href": "/assets/favicon/favicon-32x32.png", "sizes": "32x32"},
        {"href": "/assets/favicon/favicon-16x16.png", "sizes": "16x16"},
        {"href": "/assets/favicon/favicon-96x96.png", "sizes": "96x96"},
        {"href": "/assets/favicon/android-chrome-192x192.png", "sizes": "192x192"},
        {"href": "/assets/favicon/android-chrome-512x512.png", "sizes": "512x512"},
        {"href": "/assets/favicon/apple-touch-icon.png",
         "rel": "apple-touch-icon", "sizes": "180x180"},
    ],
    social_image=OG_IMAGE_URL,
    social_image_alt=OG_IMAGE_ALT,
    social_image_width=OG_IMAGE_WIDTH,
    social_image_height=OG_IMAGE_HEIGHT,
    publisher=PUBLISHER,
    same_as=SAME_AS,
)

# ============================================================================
# Visitor tracking — MUST be registered BEFORE add_llms_routes.
#
# add_llms_routes installs bot-detection middleware that answers recognised
# crawlers with its own prerendered response. A `before_request` hook added
# after it never runs for exactly the bot traffic a documentation site most
# wants counted, so the `bot_hits` reported to 2plot.ai would be quietly low.
#
# Headers are passed so the tracker can read the real client IP and country
# from the proxy: behind Render or Cloudflare, `remote_addr` is the proxy and
# every visitor would otherwise look like the same one.
# ============================================================================

from flask import request as _flask_request  # noqa: E402


@app.server.before_request
def track_visitor():
    try:
        tracker.track_visit(
            _flask_request.path,
            _flask_request.headers.get("User-Agent", ""),
            _flask_request.remote_addr,
            headers=dict(_flask_request.headers),
        )
    except Exception:  # noqa: BLE001 — analytics must never break a page view
        pass


# The hub's announcement feed, rendered in the header of this site's llms.txt
# viewer. Opt-in: with NETWORK_BULLETIN_URL unset it wires nothing and the
# viewer still renders on the package's built-in tips. The boot line says which
# of the two states this process is in — the boilerplate shipped this
# commented out for weeks against a hub endpoint that was already serving, and
# an announcement that never appears is not a symptom anyone notices.
print(
    f"[dash-email] network bulletin: "
    f"{'wired -> ' + (bulletin.url() or '') if bulletin.configure() else 'off (NETWORK_BULLETIN_URL unset)'}"
)

# ============================================================================
# Access control (dash-improve-my-llms 2.3). Reads the tiers the pages just
# declared, so it must run after they are registered and before the routes are
# attached. Stays OFF unless some page declares a non-public tier — the policy
# and the reasoning live in lib/access.py.
# ============================================================================

from lib import access as _access  # noqa: E402
from lib import page_tiers as _page_tiers  # noqa: E402
from lib import page_visibility as _page_visibility  # noqa: E402

# Tiered corpus documents (dash-improve-my-llms >= 2.4.0). Pseudo-paths:
# they never enter dash.page_registry, so they cannot leak into listings —
# registering them here lets this satellite tier its compact briefing and
# full corpus via env (LLMS_SMALL_TIER / LLMS_FULL_TIER), and the hub can
# tighten either network-wide through its page-tier ceilings with no
# redeploy here. The explicit `or "public"` matters: these registered under
# the PAGE_DEFAULT_TIER fallback before, which meant flipping that env to
# gate the *interactive* site would silently gate the corpus documents too.
# Their tier is now always a deliberate setting, never an ambient default.
_page_tiers.register("/llms-small.txt",
                     os.environ.get("LLMS_SMALL_TIER") or "public")
_page_tiers.register("/llms-full.txt",
                     os.environ.get("LLMS_FULL_TIER") or "public")

# The home page registers via pages/home.py, not pages/markdown.py, so no
# frontmatter ever declares its tier — under PAGE_DEFAULT_TIER=auth it would
# silently inherit the gate. The funnel's front door stays public, always.
_page_tiers.register("/", "public")

# The builder is this site's showcase app, registered in pages/email_builder.py
# with no frontmatter and no gate wrapper (only markdown pages render through
# lib/gate_layouts). Pinning it public keeps the tier ledger truthful: without
# this, a PAGE_DEFAULT_TIER=auth flip would list a "gated" page nothing
# actually gates.
_page_tiers.register("/email-builder", "public")

# force= when either gate env is present: with every tier still public the
# auto-detect would skip the wiring, but a host that flips by env needs the
# verdict plumbing (and the prerender's use of it) live during the dark
# launch, not on the flip.
ACCESS_ENABLED = _access.configure(
    force=bool(os.environ.get("PAGE_DEFAULT_TIER")
               or os.environ.get("LLMS_PUBLIC_DEFAULT"))
)

# Wires /llms.txt, /<page>/llms.txt, /robots.txt, /sitemap.xml and
# bot-detection middleware.
add_llms_routes(app, LLMSConfig(warn_missing_llms_doc=True))

# The ledger row (item 12, dimll 2.8.0): the package emits one event per
# corpus document it serves and does no I/O with it; the tracker keeps it
# as the `reads` table next to `visits` (lib/analytics_tracker.record_read).
# Registered ONCE — the test suite imports run.py more than once per
# process and `on_document_read` appends, so a marker on the callback's
# owner guards the second import (the package also dedups an identical
# callable; belt and braces).
if not getattr(tracker, "_read_hook_registered", False):
    on_document_read(tracker.record_read)
    tracker._read_hook_registered = True

# ============================================================================

app.layout = create_appshell(dash.page_registry.values())

server = app.server


# /healthz — Render's health check, the hub's hourly sweep, CD's build-match
# wait and scripts/network_smoke.py all read this. One payload builder for
# the whole fleet (lib/health.py), built PER REQUEST rather than closed over
# at registration: ok (the network-standard field the battery asserts on) +
# backend + dash_version + build (RENDER_GIT_COMMIT — what cd.yml's
# build-match wait polls) + app (SATELLITE_APP_KEY via the fork point —
# which satellite answered is a different question from which commit, on a
# fleet where hostnames get repointed) and, on dimll >= 2.7.0, the geo
# diagnostics block. The pre-floor-round inline route also carried `status`
# and `dash`; nothing consumed either (the battery reads `ok`, cd.yml reads
# `build`), so they retired with it. Never counted as a visit:
# lib/analytics_tracker drops /healthz at write time, because Render probes
# it far more often than anyone reads the docs.
from lib.health import register_health_route  # noqa: E402

register_health_route(app, "flask")


# ============================================================================
# The person→agent handoff: /api/agent-key turns the browser's Clerk session
# into a portable ?key= for copied llms.txt URLs (lib/agent_key.py). 204 for
# everyone until Clerk and the hub are configured — safe to mount always.
# ============================================================================

from lib.agent_key import register_agent_key_route  # noqa: E402

register_agent_key_route(app, "flask")

_non_public = sum(1 for t in _page_tiers.registered().values() if t != "public")
print(
    f"[email] interactive gate: default tier "
    f"'{os.environ.get('PAGE_DEFAULT_TIER') or 'public'}', "
    f"{_non_public} non-public page(s), machine surfaces "
    f"{'GATED' if not _page_tiers.get_llms_public('/__probe__') else 'open'} "
    f"by default (LLMS_PUBLIC_DEFAULT), access wiring "
    f"{'ON' if ACCESS_ENABLED else 'off'}, control board at "
    f"/admin/control-board ({_page_visibility.override_count()} live "
    f"override(s)) — dash-improve-my-llms {LLMS_PKG_VERSION}."
)

# Hourly signed rollup POSTed to 2plot.ai so the hub's owner-only /traffic
# dashboard can chart this app alongside the network. No-op unless
# CROSS_APP_WEBHOOK_SECRET is set. A flock lease means exactly one worker
# reports per interval rather than N racing duplicates.
from lib.satellite_reporter import start_reporter  # noqa: E402

start_reporter()


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("DASH_DEBUG", "0") == "1",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8054)),
    )
