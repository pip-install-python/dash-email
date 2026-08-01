"""
Dash Email — documentation site + AI-powered email builder.

Serves the component documentation (markdown-driven, docs/**/*.md) alongside
the /email-builder application. Run locally:

    python run.py                 # http://127.0.0.1:8054

Production (Render/Docker):

    gunicorn run:server -b 0.0.0.0:8054
"""
import os

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

from components.appshell import create_appshell  # noqa: E402
from lib import bulletin, network_directory  # noqa: E402
from lib.analytics_tracker import tracker  # noqa: E402
from lib.constants import (  # noqa: E402
    DOCS_BASE_URL,
    ORIGIN_PLACEHOLDER,
    SITE_BRAND,
    SITE_DESCRIPTION,
    require_owned_base_url,
)

from dash_improve_my_llms import (  # noqa: E402
    add_llms_routes,
    LLMSConfig,
    RobotsConfig,
    register_page_metadata,
)

print(f"[dash-email] Starting Dash {dash.__version__}")

# Refuses to boot in production if the canonical origin is a platform-generated
# hostname. `*.onrender.com` keeps resolving after the custom domain is
# attached, so a base URL pointing there splits link equity across two hosts
# and nothing about the running site looks wrong.
require_owned_base_url()

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,
    update_title=None,
    # The template's __CANONICAL_ORIGIN__ tokens become DOCS_BASE_URL here, so
    # the canonical origin, the JSON-LD urls and the llms.txt links all come
    # from lib/constants.py. A static file cannot import that module, and two
    # hand-maintained copies of an origin is exactly how half a site ends up
    # pointing at one hostname and half at another.
    index_string=open('templates/index.html').read().replace(
        ORIGIN_PLACEHOLDER, DOCS_BASE_URL
    ),
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

# The hand-rolled `interpolate_index` override that used to sit here — injecting
# a per-route <link rel="canonical"> and <meta og:url>, plus the real page title
# — has been removed. It was written against 2.0.0, which shipped neither.
#
# 2.3.3's prerender layer emits both, tagged `data-dimll-prerender="1"`, and
# rewrites <title> per route regardless of what we pass. Keeping our copy meant
# two <link rel="canonical"> tags on every browser response (the crawler path
# was already clean, because the prerenderer rebuilds that document rather than
# appending to it) and a title override that the package overwrote anyway.
#
# Canonical, og:url, og:title, og:description, the markdown `rel="alternate"`
# and the sitemap link are the package's job now. What remains ours is the
# site-level set it does not emit — og:site_name, og:locale, keywords, author —
# which lives in templates/index.html.

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
# The definition lives in lib/network_directory.py (copied from the
# boilerplate) and `peers_for()` drops this app from its own peer list.
# Must run before add_llms_routes so the routes are built with it in place.
network_directory.apply(DOCS_BASE_URL)

# The hand-written `custom_rules` block that used to live here is gone. It
# existed to counter a dash-improve-my-llms 2.0.0 bug that emitted
# `OAI-SearchBot: Disallow: /` from inside the *allow* branch; that was fixed
# upstream in 2.3.2, and requirements.txt now floors at 2.3.3. Keeping the
# workaround on top of a fixed package would emit two groups for the same
# user-agent and leave the outcome to each crawler's merge semantics.
#
# `block_ai_training=True` is correct as of 2.3.3, which buckets per vendor
# rather than per company: the training crawlers (GPTBot, ClaudeBot, CCBot, …)
# are disallowed, while the user-triggered and search fetchers — Claude-User,
# Claude-SearchBot, ChatGPT-User, OAI-SearchBot, PerplexityBot — stay allowed.
# The old reason to run `False` (blocking broke claude.ai fetches through the
# legacy aliases) no longer applies. Note that `False` does not mean "balanced":
# it never emits the training bucket at all, which silently allows training.
app._robots_config = RobotsConfig(
    block_ai_training=True,       # Disallow GPTBot, ClaudeBot, CCBot, etc.
    allow_ai_search=True,         # Allow Claude-User/-SearchBot, ChatGPT-User, ...
    allow_traditional=True,       # Allow Googlebot, Bingbot, etc.
    crawl_delay=10,
    disallowed_paths=[],
)

# `name` here is NOT a nav label — dash.register_page in pages/home.py owns
# that, and it says "Home". This is what dash-improve-my-llms 2.3.4's
# `resolve_site_title` reads first, so it is the /llms.txt H1 and the llms
# viewer's brand chip: the two surfaces an agent uses to learn what this site
# is. It published a bare "# Dash Email" until this pass — a name that matches
# no package on PyPI and no repository on GitHub.
#
# `resolve_site_title` SKIPS generic candidates ("Home", "Index", "Dash"), so
# passing the page's display name here would silently fall through to
# `app.title` instead of erroring. Nothing would look broken.
register_page_metadata(
    path="/",
    name=SITE_BRAND,
    description=SITE_DESCRIPTION,
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
# Visitor tracking — MUST be registered BEFORE add_llms_routes.
#
# add_llms_routes installs bot-detection middleware that answers recognised
# crawlers with its own prerendered response. A `before_request` hook added
# after it never runs for exactly the bot traffic a documentation site most
# wants counted, so the `bot_hits` reported to 2plot.ai would be quietly low.
# The old lib/traffic_reporter.py wiring sat at the very bottom of this file
# and had precisely that flaw.
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


# Wires /llms.txt, /<page>/llms.txt, /robots.txt, /sitemap.xml and
# bot-detection middleware.
add_llms_routes(app, LLMSConfig(warn_missing_llms_doc=True))

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

app.layout = create_appshell(dash.page_registry.values())

server = app.server


@server.route("/healthz")
def healthz():
    """Liveness probe: Render's health check, the hub's hourly sweep, CD's
    sustained-health loop and scripts/network_smoke.py all read this.

    `ok: true` is the network-standard field — the battery asserts on it, so a
    host that answers 200 with a body of some other shape reads as unhealthy
    across the whole fleet. `status` and `dash` are kept because Render's
    dashboard and the existing runbooks show them.

    Never counted as a visit: lib/analytics_tracker drops /healthz at write
    time, because Render probes it far more often than anyone reads the docs.
    """
    return {"ok": True, "status": "ok", "dash": dash.__version__}


# Hourly signed rollup POSTed to 2plot.ai so the hub's owner-only /traffic
# dashboard can chart this app alongside the network. No-op unless
# CROSS_APP_WEBHOOK_SECRET is set. A flock lease means exactly one worker
# reports per interval rather than N racing duplicates — which the previous
# hand-rolled reporter did not have, and which only stayed invisible because
# render.yaml pins WEB_WORKERS=1.
from lib.satellite_reporter import start_reporter  # noqa: E402

start_reporter()


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("DASH_DEBUG", "0") == "1",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8054)),
    )
