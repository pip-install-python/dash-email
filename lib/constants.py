import os

# ---------------------------------------------------------------------------
# Site identity — one string, every surface
# ---------------------------------------------------------------------------
# The network standard (2plot.ai, 2plot.dev, boilerplate.2plot.dev and
# leaflet.2plot.dev all ship it): a site states what it is, in the same words,
# on every surface an agent or a reader can reach. The surfaces this brand has
# to reach, and what serves each:
#
#   Dash(title=SITE_BRAND)              -> <title>, and the fallback identity
#   register_page_metadata(path="/",    -> the /llms.txt H1 and the llms
#       name=SITE_BRAND)                   viewer's brand chip, both via
#                                          dash-improve-my-llms 2.3.4's
#                                          `resolve_site_title`
#   pages/home.py's LLMS_DOC H1         -> the home page's own prose
#
# tests/test_site_identity.py pins all of them to this constant, because the
# failure is silent: `resolve_site_title` SKIPS generic candidates ("Home",
# "Index", Dash's default "Dash") rather than publishing them, so a site that
# never states its identity falls through to whatever is left and nothing looks
# broken. This host published a bare "# Dash Email" as its /llms.txt H1 — not a
# framework default, but not the network's identity either: it named the site
# after nothing an agent could install or search for.
#
# Naming rules, from the network standard:
#   - "Pip Install Python" is the byline (who made it), never the site name;
#   - the package name leads, because for a component library the package IS
#     what a reader came to find. Same shape as leaflet.2plot.dev
#     ("dash-leaflet2 — Leaflet 2 maps for Dash"). The boilerplate keeps its
#     package name out of its brand for the opposite reason: nobody installs a
#     template.
SITE_BRAND = "dash-email — email components for Dash"

SITE_DESCRIPTION = (
    "dash-email — 15 email-safe Plotly Dash components wrapping React Email "
    "patterns. Build, preview and send HTML emails from Python: Email, "
    "EmailBody, EmailContainer, EmailSection, EmailRow, EmailColumn, "
    "EmailHeading, EmailText, EmailButton, EmailLink, EmailImage, "
    "EmailDivider, EmailFont, EmailHead and EmailPreview. By Pip Install "
    "Python."
)

# The brand without its tagline. SITE_BRAND is right for a page that has room
# for it; this is for the places that prefix something else and would otherwise
# run past every platform's truncation point.
SITE_SHORT_NAME = "dash-email"

# Prefixed to every per-page title (`pages/markdown.py`, `pages/home.py`), and
# therefore NOT only a browser-tab string: Dash passes the page title straight
# into `og:title` and `twitter:title` (dash/_pages.py `_page_meta_tags`), so
# this is the headline on every share card the site produces.
#
# Derived rather than retyped so the two cannot drift apart;
# tests/test_site_identity.py pins the relationship. It read "Dash Email | "
# until this pass — a name that matches no package on PyPI and no repo on
# GitHub, so every unfurl advertised a thing that could not be looked up.
PAGE_TITLE_PREFIX = f"{SITE_SHORT_NAME} | "

PRIMARY_COLOR = "blue"

# Keep in step with package.json and dash_email/package.json when cutting a
# release — scripts/check_release.py fails the build if the three disagree.
APP_VERSION = "0.2.1"

GITHUB_URL = "https://github.com/pip-install-python/dash-email"

# The package cross-link block — who publishes this site, and which other
# URLs are the same entity. `SAME_AS` becomes JSON-LD `sameAs` on every
# crawler page (run.py passes both to `configure_seo`): for a docs satellite
# it should list the documented package's GitHub repo and PyPI project —
# three properties pointing at each other is the strongest statement of which
# URL is a package's canonical docs home.
PUBLISHER = "Pip Install Python LLC"
SAME_AS = [
    GITHUB_URL,
    "https://pypi.org/project/dash-email/",
]

# ---------------------------------------------------------------------------
# Navigation contract (item 16, ported from the template's 1.6.41) — the
# parts of the sidebar/top bar that are IDENTICAL on every host come from
# template code and these constants; this app's own sections (Getting
# started, App, Components, Templates) come from each page's frontmatter
# `category:`. A fork edits THIS block and its docs' frontmatter, never
# components/navbar.py.
#
# PER-FORK IDENTITY: dash-email keeps "App" (the Email Builder) as its own
# top-level sidebar category rather than folding it into "Components" — the
# builder is this site's showcase application, not a documented component.
# ---------------------------------------------------------------------------

# The app's own sections, in sidebar order. Every docs page declares
# `category:` in its frontmatter (pages/email_builder.py declares its own
# category= directly at register_page, since it has no frontmatter file);
# categories not listed here follow the listed ones, alphabetically.
CATEGORY_ORDER = [
    "Getting started",
    "App",
    "Components",
    "Templates",
]

# Network-wide community links — identical on every host.
DISCORD_URL = "https://discord.gg/e5s5uHWUHH"
YOUTUBE_URL = "https://www.youtube.com/@2plotai"
YOUTUBE_SUBSCRIBE_URL = YOUTUBE_URL + "?sub_confirmation=1"
DMC_URL = "https://www.dash-mantine-components.com/"

# The upstream project this component library wraps. Rendered as the last
# Resources link (lib.constants.resources()). dash-email wraps React Email;
# Resend (the transactional-send API the Email Builder sends through) is
# deliberately NOT declared a second upstream here — this constant is
# singular in the template's contract, and React Email is what the
# COMPONENTS document (Resend is a sending integration used by the builder,
# not something dash-email's components wrap). A link to Resend still lives
# on the Email Builder's own page.
UPSTREAM = {"name": "React Email", "url": "https://react.email/docs",
            "icon": "simple-icons:react"}

# Dash component packages whose props the generated /api page documents.
# The version badge in the header reads the first entry's __version__.
API_PACKAGES: list = ["dash_email"]

# The owner's profile — the FOOTER's GitHub link (the repo is the top bar's).
GITHUB_PROFILE_URL = "https://github.com/pip-install-python"

# The header's mark (1.6.41 shape): the asset under assets/, its box, the
# wordmark colour, and the breakpoint the wordmark text appears from. Kept
# here rather than hardcoded in components/header.py so a fork edits one
# place for its whole header identity.
WORDMARK = "dash-email"
LOGO_ASSET = "email-logo.png"
LOGO_STYLE = {"height": "32px", "width": "32px"}
WORDMARK_COLOR = "#228be6"
WORDMARK_VISIBLE_FROM = "xs"


def resources() -> list:
    """The sidebar's Resources section: THIRD-PARTY ONLY. `dmc` and the
    declared upstream (React Email). The owner's own links (repo, Discord,
    YouTube) live in the top bar and the footer, never here; no
    community.plotly.com; no 2plot.dev (the network is the Other Apps
    menu)."""
    items = [
        {"label": "dmc", "url": DMC_URL, "icon": "ic:baseline-design-services"},
    ]
    if UPSTREAM:
        items.append({"label": UPSTREAM["name"], "url": UPSTREAM["url"],
                      "icon": UPSTREAM.get("icon", "mdi:open-in-new")})
    return items


# Height of the fixed AppShell header, in px. Consumed by AppShell(header=...)
# and by the mobile drawer, which docks itself directly below the header.
# Change it here only — the two must never drift apart.
HEADER_HEIGHT = 70

# ---------------------------------------------------------------------------
# Public origin
# ---------------------------------------------------------------------------
# The single source of truth for every absolute URL this app emits: sitemap.xml,
# robots.txt, the llms.txt links, and the per-page <link rel="canonical">.
# templates/index.html does NOT restate it — run.py substitutes it into the
# template's __CANONICAL_ORIGIN__ token at startup, so there is nothing to drift.
#
# TWO env names, on purpose. `APP_BASE_URL` is the network-wide name every
# other satellite reads (the boilerplate, leaflet, the hub), and it wins;
# `DASH_EMAIL_BASE_URL` is this repo's original name and is still honoured
# because render.yaml has been setting it in production since the first deploy.
# Renaming it in one place and not the other is how a host quietly starts
# advertising the wrong canonical origin.
#
# Leaving both unset in production is correct: the default is the canonical
# public origin, which is what consolidates link equity onto one hostname
# instead of splitting it with *.onrender.com.
DEFAULT_BASE_URL = "https://email.2plot.dev"
DOCS_BASE_URL = (
    os.environ.get("APP_BASE_URL")
    or os.environ.get("DASH_EMAIL_BASE_URL")
    or DEFAULT_BASE_URL
).rstrip("/")

# Kept as an alias because the network's shared files (scripts/, tests/) import
# `BASE_URL` by that name on every host. One value, two spellings, no second
# source of truth.
BASE_URL = DOCS_BASE_URL

# Token in templates/index.html that run.py swaps for DOCS_BASE_URL at startup.
# The template is a static file, so it cannot read this module; the substitution
# is what keeps one origin rather than two that can disagree.
ORIGIN_PLACEHOLDER = "__CANONICAL_ORIGIN__"

# ---------------------------------------------------------------------------
# The social card
# ---------------------------------------------------------------------------
# Dash builds `og:image` and `twitter:image` for every page from
# `register_page(image_url=...)`, and emits `content=""` when it finds neither
# an explicit URL nor an inferable asset (dash/_pages.py). This site had no
# brand image, so every page shipped an EMPTY og:image — which unfurls WORSE
# than having no tag at all, because scrapers treat the empty value as the
# declared image and render a blank card. Nobody sees their own unfurls, so it
# had been live since the first deploy.
#
# `image_url` takes an absolute URL and wins over the assets-derived one, so
# passing it at `register_page` time fixes every page at the source instead of
# fighting tag order inside templates/index.html.
#
# THE CARD LIVES ON THE CDN, NOT IN assets/. Network rule, and it is about cold
# starts rather than tidiness: a card served by the app is fetched by the
# scraper at unfurl time, and on a cold free-tier container that request lands
# mid-wake and times out. The preview renders blank ONCE and the platform
# caches the miss — so the first person to share the link poisons it for
# everyone. The CDN has no cold start.
#
# Rendered by `scripts/make_social_card.py` (1200x630 = 1.91:1, the Open Graph
# ideal, which also degrades cleanly into Twitter's 2:1 slot) and uploaded by
# hand to the Cloudflare bucket. There is no automated path to that bucket.
#
# The width and height MUST match the file. A declared size that disagrees is
# worse than declaring none, because the platform reserves that box and crops
# into it. `tests/test_social_card.py` pins these against
# `templates/index.html`, and `scripts/smoke_live.py` fetches the real file
# after every deploy and reads its IHDR chunk — the only check that can catch
# the CDN object being replaced with something a different shape.
OG_IMAGE_URL = "https://cdn.2plot.ai/github_assets/email.2plot.dev.png"
OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630
OG_IMAGE_TYPE = "image/png"
OG_IMAGE_ALT = SITE_BRAND

# ---------------------------------------------------------------------------
# The network's internal-traffic contract
# ---------------------------------------------------------------------------
# The analytics point of truth is https://2plot.ai/docs/satellite-analytics
# ("Internal traffic"): any request whose User-Agent contains
# INTERNAL_UA_TOKEN is 2plot network machinery talking to itself — the hub's
# hourly health sweep, CI smoke batteries, the 4x-daily heartbeat, this app's
# own server-to-server calls to the hub. It is counted NOWHERE.
#
# Two halves, and both are required for the contract to hold:
#
#   inbound  — every tracker drops a token-carrying request at WRITE time,
#              before device detection and before bot classification, so it
#              never reaches the ledger the hourly rollup is built from;
#   outbound — every call this host makes to another network host sends
#              INTERNAL_UA, so the far side can apply the same rule.
#
# The outbound half is the one that was missing here. lib/ad_client.py fetched
# campaigns from 2plot.dev as bare `python-requests`, once per docs page view,
# which the hub's own tracker classifies as a bot — every reader of these docs
# was inflating 2plot.dev's bot_hits. lib/satellite_reporter.py had the same
# shape, once per host per hour, forever.
#
# The token string must stay byte-identical across the network; it mirrors
# 2plotai/lib/constants.py, pip-docs+/lib/constants.py, the boilerplate's and
# leaflet's.
INTERNAL_UA_TOKEN = "2plot-internal"
INTERNAL_UA = "2plot-internal/1.0 (+https://2plot.ai/docs/satellite-analytics)"


def internal_ua(caller: str = "") -> str:
    """``INTERNAL_UA`` with a caller suffix, e.g. ``"ad-client"``.

    The suffix is for reading logs on the far side; only the token matters to
    the contract, and it stays intact whatever the suffix says.
    """
    caller = (caller or "").strip()
    return f"{INTERNAL_UA} {caller}" if caller else INTERNAL_UA


def require_owned_base_url(base_url: str = DOCS_BASE_URL) -> None:
    """Fail fast in production when the base URL isn't this app's real origin.

    Only enforced when a hosting platform is detected (Render sets ``RENDER``;
    ``APP_ENV=production`` works anywhere else), so local development and the
    test suite are unaffected.

    Unlike the boilerplate's copy this does NOT require the env var to be set:
    ``DEFAULT_BASE_URL`` here is this app's own origin rather than a template's,
    so inheriting it is correct. What is still caught is the failure that
    actually bites — a platform-generated hostname. ``*.onrender.com`` keeps
    resolving after a custom domain is attached, so canonicals pointing there
    split link equity across two hosts for as long as nobody notices.
    """
    in_production = bool(
        os.environ.get("RENDER") or os.environ.get("APP_ENV") == "production"
    )
    if not in_production:
        return

    for platform_host in ("onrender.com", "herokuapp.com", "railway.app", "fly.dev"):
        if platform_host in base_url:
            raise RuntimeError(
                f"base URL {base_url!r} is a platform-generated hostname. "
                "Canonical tags, sitemap.xml and llms.txt would all point at it "
                "instead of the custom domain, splitting link equity across two "
                "hosts. Set APP_BASE_URL to the public domain."
            )


# Populated by pages/markdown.py when loading documentation files.
# Maps page name -> raw markdown content (used by the llms_copy directive).
NAME_CONTENT_MAP = {}
