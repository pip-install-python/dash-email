import os

PAGE_TITLE_PREFIX = "Dash Email | "
PRIMARY_COLOR = "blue"
APP_VERSION = "0.2.0"

GITHUB_URL = "https://github.com/pip-install-python/dash-email"

# The single source of truth for every absolute URL this app emits: sitemap.xml,
# robots.txt, the llms.txt links, and the per-page <link rel="canonical">.
# templates/index.html does NOT restate it — run.py substitutes it into the
# template's __CANONICAL_ORIGIN__ token at startup, so there is nothing to drift.
#
# Override with DASH_EMAIL_BASE_URL when the app is reachable somewhere else
# (a preview deploy, a staging host). Leaving it unset in production is correct:
# the default is the canonical public origin, which is what consolidates link
# equity onto one hostname instead of splitting it with *.onrender.com.
DEFAULT_BASE_URL = "https://email.2plot.dev"
DOCS_BASE_URL = (os.environ.get("DASH_EMAIL_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")

# Token in templates/index.html that run.py swaps for DOCS_BASE_URL at startup.
# The template is a static file, so it cannot read this module; the substitution
# is what keeps one origin rather than two that can disagree.
ORIGIN_PLACEHOLDER = "__CANONICAL_ORIGIN__"

# Populated by pages/markdown.py when loading documentation files.
# Maps page name -> raw markdown content (used by the llms_copy directive).
NAME_CONTENT_MAP = {}
