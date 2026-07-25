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

from components.appshell import create_appshell
from lib.constants import DOCS_BASE_URL
from lib.traffic_reporter import register_traffic_reporting

from dash_improve_my_llms import (
    add_llms_routes,
    LLMSConfig,
    RobotsConfig,
    register_page_metadata,
)

load_dotenv()

print(f"[dash-email] Starting Dash {dash.__version__}")

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,
    update_title=None,
    index_string=open('templates/index.html').read(),
)

# ============================================================================
# AI/LLM & SEO configuration (dash-improve-my-llms)
# ============================================================================

app._base_url = DOCS_BASE_URL

app._robots_config = RobotsConfig(
    block_ai_training=False,
    allow_ai_search=True,
    allow_traditional=True,
    crawl_delay=10,
    disallowed_paths=[],
)

register_page_metadata(
    path="/",
    name="Dash Email",
    description=(
        "A Plotly Dash component library wrapping React Email patterns: "
        "15 email-safe components for building, previewing, and sending "
        "HTML emails from Python."
    ),
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

# Wires /llms.txt, /<page>/llms.txt, /robots.txt, /sitemap.xml and
# bot-detection middleware.
add_llms_routes(app, LLMSConfig(warn_missing_llms_doc=True))

# ============================================================================

app.layout = create_appshell(dash.page_registry.values())

server = app.server


@server.route("/healthz")
def healthz():
    return {"status": "ok", "dash": dash.__version__}


# Reports this app's hourly traffic rollup to 2plot.ai's /traffic hub —
# see lib/traffic_reporter.py for the contract.
register_traffic_reporting(app)


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("DASH_DEBUG", "0") == "1",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8054)),
    )
