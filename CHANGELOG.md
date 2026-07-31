# Changelog

All notable changes to **dash-email** are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

`release.yml` extracts the section matching the tag being pushed and attaches
it to the GitHub Release, so the heading format `## [X.Y.Z] — YYYY-MM-DD`
matters.

## [Unreleased]

### Changed

- **Migrated onto `dash-improve-my-llms` 2.3.3 and the 2plot network**
  (`handoff/existing_subdomains.md`). dash-email is the first repo through this
  migration, so several findings below are fleet-wide rather than local.
  - Floor bumped `>=2.0.0` → `>=2.3.3` in `requirements.txt`.
  - **Deleted the hand-written OAI-SearchBot `custom_rules` block.** It
    countered a 2.0.0 bug fixed upstream in 2.3.2; kept on top of a fixed
    package it emits two groups for one user-agent.
  - **`block_ai_training=True`.** 2.3.3 buckets per vendor, so the training
    crawlers (GPTBot, ClaudeBot, CCBot) are disallowed while the user-triggered
    and search fetchers (Claude-User, Claude-SearchBot, ChatGPT-User,
    OAI-SearchBot, PerplexityBot) stay allowed — verified, not assumed.
  - **Cross-host network directory** — `lib/network_directory.py` plus
    `network_directory.apply()` before `add_llms_routes`, so `/llms.txt` now
    carries a `## Network` section. `lib/hub_client.py` skipped: dash-email has
    no access tiers.
  - **Analytics chain replaced** — `lib/traffic_reporter.py` (hand-rolled) out;
    `analytics_tracker.py` + `traffic_rollup.py` + `satellite_reporter.py` in.
    Adds a flock lease so exactly one worker reports per interval.
  - **Visitor tracking moved above `add_llms_routes`.** The package's bot
    middleware answers recognised crawlers itself, so the old bottom-of-file
    hook never ran for bot traffic and `bot_hits` was silently undercounting.

### Fixed

- **Retired the 2.0-era canonical/title shim.** 2.3.3 prerenders
  `<link rel="canonical">`, `og:*` and a per-page `<title>`, so the
  `interpolate_index` override added for 2.0.0 produced **two** canonical tags
  on every browser response, and its title was overwritten by the package
  anyway. The client-side sync script is now update-only, so it can never
  create a second one.

### Notes for the fleet

Three things found here that are **not** dash-email bugs:

- **`bot_detection` misses `facebookexternalhit` and `Claude-User`.** Neither
  string appears in the package, so `is_any_bot()` returns False and neither
  gets the prerendered document — including the canonical. `Claude-User` is
  ironic: robots.txt explicitly *allows* it. Belongs in `dash-hook-my-ai`.
- **The boilerplate's `lib/network_directory.py` lists two dead peers.**
  `pannellum.2plot.dev` and `emojimart.2plot.dev` are NXDOMAIN as of
  2026-07-31; `llms.2plot.dev` is live but absent. Trimmed locally with a
  comment; the fix belongs upstream since that file is copied to every
  satellite. The hub's `SATELLITES` table is stale in the other direction —
  `muischeduler` and `flows` are marked `shipping` but both resolve.
- **`grep -c "requires JavaScript"` can never return 0** on 2.3.3. The
  runbook lists it as a verification step, but the package emits
  "Interactive version requires JavaScript." in its own crawler-facing footer.

## [0.2.0] — 2026-07-29

First release with a measured support claim and an automated release path.

### Added

- **Dash 4.1+ support, verified rather than asserted.** `scripts/compat_matrix.py`
  builds one environment per Dash version and runs the full smoke suite in each;
  results land in [COMPATIBILITY.md](./COMPATIBILITY.md). 4.1.0 / 4.2.0 / 4.3.0 /
  4.4.1 all pass.
- **`scripts/smoke_test.py`** — 59-check headless suite driving the whole app
  through Flask's test client: the 15-component package surface, a full email
  template through Dash's JSON encoder, page registration, every layout
  rendered, every route plus `/healthz`, `/llms.txt`, `/robots.txt` and
  `/sitemap.xml` fetched, every inline clientside callback syntax-checked with
  node, and `assets/*.js` parsed both individually and concatenated.
- **`scripts/check_release.py`** — pre-tag consistency: version drift across
  `package.json`, `dash_email/package.json` and `lib/constants.py`, a stale or
  missing JS bundle, a React component with no generated Python class, and
  packaging drift.
- **GitHub Actions CI** (`.github/workflows/ci.yml`) — the smoke matrix across
  Dash 4.1 → 4.4.1, a wheel build installed into a clean venv with nothing but
  Dash present, and an import + layout build on Python 3.9 → 3.13.
- **GitHub Actions Release** (`.github/workflows/release.yml`) — tag-driven
  publish to PyPI via OIDC trusted publishing, with a TestPyPI dry-run mode.
  No API token is stored anywhere.
- **[RELEASING.md](./RELEASING.md)** — the runbook from a clean tree to a
  published version.
- **Video demo** — linked from the README, and embedded on the home page
  directly above *Features* as a responsive 16:9 `youtube-nocookie.com` player
  (no tracking cookie until the viewer presses play, so the docs need no
  consent banner).
- **Custom domain `https://email.2plot.dev`.** `render.yaml` declares it on the
  service alongside `DASH_EMAIL_BASE_URL`, and the deploy runbook covers the
  CNAME plus the three network-registration steps that each fail silently.
  The `*.onrender.com` hostname keeps working but is no longer the canonical
  origin, so hits on it consolidate onto the custom domain instead of
  competing with it.
- **One source of truth for the origin.** `DEFAULT_BASE_URL` in
  `lib/constants.py` (overridable per environment with `DASH_EMAIL_BASE_URL`)
  now feeds everything: `templates/index.html` carries `__CANONICAL_ORIGIN__`
  tokens that `run.py` substitutes at startup, so the canonical link, `og:url`,
  the JSON-LD, `sitemap.xml`, `robots.txt` and the llms.txt links cannot
  disagree. `check_release.py` fails if a literal origin is pasted back into
  the template or `render.yaml` stops serving the canonical host.
- **An `[seo]` check group in the smoke suite** — nine checks covering every
  head-tag bug listed under *Fixed* below, so none of them can silently
  return. Each one was verified to fail when the original bug is reintroduced.

### Fixed

Search-engine and social metadata. `templates/index.html` came from
dash-documentation-boilerplate and, while it had been renamed for this project,
its structure still fought Dash's own per-page tags:

- **Every route served `<title>Dash</title>`.** Dash interpolates `{%title%}`
  with `app.title` and resolves the per-page title only in the browser, so
  anything that does not execute JavaScript — most crawlers, every link
  unfurler — saw the same meaningless title on all 11 pages. `run.py` now
  overrides `interpolate_index` to substitute the real page title server-side,
  with a proper product name as the fallback for unmatched paths.
- **`<link rel="canonical">` was hard-coded to the site root**, so ten of the
  eleven pages declared themselves duplicates of the eleventh. This is the one
  that does real damage — it is how a domain gets dropped from the index.
  It is now resolved per request from the page registry, so the raw HTML
  carries the correct canonical for non-rendering crawlers, and a script keeps
  it (plus `og:url` and `twitter:url`) in sync across Dash's client-side
  navigation. Paths outside the registry get no canonical at all.
- **Seven duplicated tags removed.** `register_page()` makes Dash emit
  per-page `description`, `og:title`, `og:type`, `og:description`, `og:image`
  and the full `twitter:*` set. The template restated all of them at site
  level — strictly worse, because engines choose between duplicates blind.
  Only `og:site_name`, `og:locale`, `keywords` and `author` remain, being tags
  Dash does not emit.
- **The encoding declaration sat at byte 1327**, outside the 1024-byte window
  the HTML spec requires it in. Dash's own `<meta charset>` was at byte 1008
  on the longest page — conforming, but with 16 bytes to spare. `charset` is
  now the first thing in `<head>`, pinned near byte 60 whatever Dash prepends.
- **robots.txt was blocking ChatGPT Search.** `dash-improve-my-llms` 2.0.0
  emits `Disallow: /` for `OAI-SearchBot` from inside its
  `if config.allow_ai_search:` branch, under a heading reading "Allow AI
  Search and Citation Bots", while its three siblings get `Allow: /`. Worked
  around by supplying the corrected group through `custom_rules`. **This is an
  upstream bug and affects every site using that library** — the workaround
  should be removed once it is fixed there.
- **Structured data retyped** from `SoftwareApplication` to
  `SoftwareSourceCode`, which is what an importable library is, plus a
  `WebSite` node. Every value is checked against the actual package; no
  ratings, prices or download counts that nothing measures.

- **`load_dotenv()` ran too late to have any effect.** It sat below the
  first-party imports in `run.py`, but `lib/constants.py`, `lib/ad_client.py`
  and `lib/traffic_reporter.py` all read `os.environ` at *import* time — so
  `AD_SERVER_URL`, `AD_APP_ID`, `SATELLITE_APP_KEY` and `TRAFFIC_REPORT_URL`
  silently ignored `.env` and used their defaults. Render passes real process
  environment variables, which is precisely why this never showed up in
  production.

`og:image` is deliberately left empty rather than pointed at an invented file —
an empty tag beats a 404 in a link preview. The template documents exactly what
to add (`assets/og-image.png` at 1200×630, plus `image=` on `register_page`).

### Changed

- **Dash floor lowered from 4.2.0 to 4.1** in `setup.py` and `requirements.txt`.
  Nothing in the library or the docs site used a 4.2-only API; the old floor was
  asserted, not measured, and the matrix now proves 4.1 works.
- The `More from Pip Install Python LLC` table in the README now lists the full
  network: 2plot.ai, 2plot.media, 2plot.dev, ai-agent.buzz and PiratesBargain.

## [0.0.1] — 2026-07-24

Initial release.

### Added

- 15 email-safe Dash components wrapping React Email patterns: `Email`,
  `EmailHead`, `EmailPreview`, `EmailBody`, `EmailContainer`, `EmailSection`,
  `EmailRow`, `EmailColumn`, `EmailHeading`, `EmailText`, `EmailButton`,
  `EmailLink`, `EmailImage`, `EmailDivider`, `EmailFont`.
- Markdown-driven documentation site with live examples, props tables and
  `/<page>/llms.txt` on every page.
- `/email-builder` — AI template generation via Google Gemini, live preview,
  Python export, and single/batch/scheduled sending through Resend.
- Render blueprint (`render.yaml`) + `Dockerfile` with a `/healthz` check.
- Dark-mode-faithful rendering of email examples in the docs.
- 2plot.ai satellite traffic reporting.
- Graceful boot without a Gemini API key (builder showcase mode).
