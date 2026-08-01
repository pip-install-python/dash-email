<div align="center">

<!-- Absolute CDN URL, not a repo-relative path: this README is also the PyPI
     long_description, where a relative image 404s. -->
<a href="https://2plot.ai">
  <img src="https://cdn.2plot.ai/github_assets/light_mode_2plot.png" alt="2plot.ai" width="320">
</a>

# dash-email — email components for Dash

**Email components for [Plotly Dash](https://dash.plotly.com), wrapping [React Email](https://react.email) patterns.**

15 email-safe components · table-based layouts · AI-powered builder · live preview · send via Resend · full Dash callback interoperability.

[![PyPI version](https://img.shields.io/pypi/v/dash-email?color=blue)](https://pypi.org/project/dash-email/)
[![Python](https://img.shields.io/pypi/pyversions/dash-email)](https://pypi.org/project/dash-email/)
[![Dash 4.1+](https://img.shields.io/badge/Dash-4.1%2B-1a1a2e?logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![CI](https://github.com/pip-install-python/dash-email/actions/workflows/ci.yml/badge.svg)](https://github.com/pip-install-python/dash-email/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white)](https://discord.gg/WEnZR35mrK)
[![YouTube](https://img.shields.io/badge/YouTube-%402plotai-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/channel/UC6Bmo0t0ZUpU_xKBYW0bJuQ)

**[Documentation](https://email.2plot.dev)** · [Discord](https://discord.gg/WEnZR35mrK) · [YouTube](https://www.youtube.com/channel/UC6Bmo0t0ZUpU_xKBYW0bJuQ) · [GitHub](https://github.com/pip-install-python/dash-email)

<br/>

### ▶️ Video demo

[![Dash Email: Build, Preview & Send Emails Inside Your Dash App](https://img.youtube.com/vi/_30EHZ1-2vs/maxresdefault.jpg)](https://youtu.be/_30EHZ1-2vs)

**[Dash Email: Build, Preview & Send Emails Inside Your Dash App](https://youtu.be/_30EHZ1-2vs)** — the components, the live preview, and the AI builder end to end.

<br/>

_Maintained by **[Pip Install Python LLC](https://pip-install-python.com)**._

</div>

---

## Overview

**dash-email** bridges Python-first development with the component patterns pioneered by [React Email](https://react.email). Build email templates with familiar Dash syntax, preview them live in your app, and export inline-styled, table-based HTML that renders correctly in Gmail, Outlook, Apple Mail, and every other major client.

- **15 email-safe components** — structure, layout, typography, buttons, images, fonts — everything a professional email needs.
- **Email-client compatible by construction** — rows and columns render as real HTML tables; all styling is inlined.
- **First-class Dash citizens** — every component takes an `id` and works with callbacks like any other Dash component.
- **AI-powered builder** — the bundled `/email-builder` app generates templates from a plain-English prompt via Google Gemini and exports ready-to-paste Python.
- **Send & schedule** — integrated [Resend](https://resend.com) support for single sends, batches up to 100 recipients, and scheduling.

> ⚠️ dash-email is in early release (0.x). The component API is stable, but the AI builder and sending utilities are actively evolving. See [CHANGELOG.md](./CHANGELOG.md) for what has shipped.

## Installation

```bash
pip install dash-email
```

Requires `dash>=4.1`. See [Dash compatibility](#dash-compatibility) for the tested matrix.

## Quick Start

```python
import dash
import dash_email as de

app = dash.Dash(__name__)

app.layout = de.Email(
    lang="en",
    children=[
        de.EmailBody(
            style={"backgroundColor": "#f6f9fc", "padding": "40px 0"},
            children=[
                de.EmailContainer([
                    de.EmailSection(
                        style={"backgroundColor": "#ffffff", "borderRadius": "8px", "padding": "40px"},
                        children=[
                            de.EmailHeading("Welcome!", as_="h1"),
                            de.EmailText("Thanks for signing up. We're excited to have you!"),
                            de.EmailButton(
                                "Get Started",
                                href="https://example.com",
                                style={
                                    "backgroundColor": "#228be6",
                                    "color": "#ffffff",
                                    "padding": "12px 24px",
                                    "borderRadius": "4px",
                                    "fontWeight": "bold",
                                },
                            ),
                        ],
                    )
                ])
            ],
        )
    ],
)

if __name__ == "__main__":
    app.run(debug=True)
```

## Documentation

### 📚 **[email.2plot.dev](https://email.2plot.dev)**

Run the full documentation site — component pages with isolated live examples, props tables, and the AI email builder — locally:

```bash
git clone https://github.com/pip-install-python/dash-email.git
cd dash-email
pip install -r requirements.txt
# markdown2dash pins gunicorn<22, against the CVE-driven gunicorn>=23 floor in
# requirements.txt. pip cannot resolve both, so it installs without its
# dependency graph — every one of them is in requirements.txt already.
pip install --no-deps markdown2dash==0.1.2
python run.py    # http://127.0.0.1:8054
```

The site covers Getting Started, Email Structure, Container & Section, Rows & Columns, Heading & Text, Button & Link, Image & Divider, Custom Fonts, Full Templates, and the `/email-builder` app. Every docs page also serves an LLM-friendly version at `/<page>/llms.txt`.

## Components

| Component        | Category  | What it is                                                        |
|------------------|-----------|-------------------------------------------------------------------|
| `Email`          | Structure | Root wrapper for the email template                               |
| `EmailHead`      | Structure | Metadata container (font imports, etc.)                           |
| `EmailPreview`   | Structure | Inbox preview text — visible next to the subject, hidden in body  |
| `EmailBody`      | Structure | Main content wrapper                                              |
| `EmailContainer` | Layout    | Centered container at the 600px email standard                    |
| `EmailSection`   | Layout    | Groups related content with its own background/padding            |
| `EmailRow`       | Layout    | Horizontal row — renders as an HTML `<table>`                     |
| `EmailColumn`    | Layout    | Column within a row — renders as a `<td>`                         |
| `EmailHeading`   | Content   | Headings `h1`–`h6` via the `as_` prop                             |
| `EmailText`      | Content   | Paragraph text                                                    |
| `EmailButton`    | Content   | Bulletproof call-to-action button (styled anchor)                 |
| `EmailLink`      | Content   | Inline hyperlink                                                  |
| `EmailImage`     | Media     | Image with explicit dimensions                                    |
| `EmailDivider`   | Media     | Horizontal rule separator                                         |
| `EmailFont`      | Media     | Web font loading with graceful fallback                           |

## The styling boundary

Email clients are not browsers: they strip `<style>` tags and ignore most modern CSS. Every dash-email component takes a `style` dict of camelCase CSS that is rendered **inline** on the element, and multi-column layout goes through `EmailRow`/`EmailColumn` tables — the only layout primitive that survives every client.

```python
de.EmailRow([
    de.EmailColumn(style={"width": "70%"}, children=[de.EmailText("Product")]),
    de.EmailColumn(style={"width": "30%", "textAlign": "right"}, children=[de.EmailText("$99.00")]),
])
```

Keep content at 600px or less (`EmailContainer` does this for you), prefer web-safe fonts or `EmailFont` with a fallback, and always set explicit `width`/`height` + `alt` on `EmailImage`.

## AI Email Builder

The repository doubles as a full application. `/email-builder` generates templates from a description — 18 email types across marketing, transactional, and professional categories — previews them live, exports `dash_email` Python code, and sends via Resend.

```bash
# .env
GOOGLE_API_KEY=your_google_api_key   # AI generation (Google Gemini)
RESEND_API_KEY=re_your_api_key       # sending (optional)
```

Both keys are optional: the docs run without them and the builder degrades gracefully.

## API reference

### Selected props

| Prop       | Type   | Description                                                       |
|------------|--------|-------------------------------------------------------------------|
| `id`       | str    | Dash callback identity — available on every component             |
| `style`    | dict   | camelCase CSS, rendered inline for email-client safety            |
| `children` | node   | Child components / text                                           |
| `as_`      | str    | `EmailHeading` level: `"h1"`–`"h6"` (Python-safe alias for `as`)  |
| `href`     | str    | `EmailButton` / `EmailLink` target URL                            |
| `src`, `alt`, `width`, `height` | — | `EmailImage` essentials                       |
| `fontFamily`, `fallbackFontFamily`, `webFont` | — | `EmailFont` configuration       |

Full auto-generated props tables live on each component's documentation page.

## Dash compatibility

`dash-email` targets **Dash 4.1 and up**. That range is verified, not assumed —
`scripts/compat_matrix.py` builds a throwaway virtualenv per Dash version, installs the
full documentation site into each, and runs the smoke suite there:

```bash
python scripts/compat_matrix.py                    # 4.1.0, 4.2.0, 4.3.0, 4.4.1
python scripts/compat_matrix.py 4.4.1 --backends flask fastapi
python scripts/compat_matrix.py --local            # offline: use interpreters you already have
```

Results land in [COMPATIBILITY.md](./COMPATIBILITY.md) — all four versions currently pass
59/59. The per-version harness is `scripts/smoke_test.py`, which also runs standalone:

```bash
python scripts/smoke_test.py
```

It checks that all 15 components are exported and that a full email template survives
Dash's JSON encoder; that every markdown page registered a route with no duplicate paths;
that every page layout builds and serialises; that every route plus `/_dash-layout`,
`/_dash-dependencies`, `/healthz`, `/llms.txt`, `/robots.txt` and `/sitemap.xml` answers
over Flask's test client; that every inline clientside callback, every `assets/*.js` file,
and the committed component bundle all parse under `node --check`; and an `[seo]` group
asserting every route serves its own `<title>` and exactly one correct `<link
rel="canonical">` in the raw HTML, that no head tag Dash already emits is duplicated, that
the charset declaration falls inside the spec's first 1024 bytes, that `robots.txt`
contains no self-contradicting group, and that the sitemap covers every route. No socket,
no browser.

The same matrix runs in [GitHub Actions](.github/workflows/ci.yml) on every push and PR,
which additionally builds the wheel, installs it into a clean venv with **nothing but
Dash present**, and imports it on Python 3.9 → 3.13.

## Development

```bash
git clone https://github.com/pip-install-python/dash-email.git
cd dash-email

# JS toolchain (only needed when changing src/lib/components)
npm install
npm run build          # webpack bundle → dash_email/dash_email.min.js
npm run extract-meta   # regenerate Python wrappers → dash_email/*.py

# Python
pip install -r requirements.txt
pip install --no-deps markdown2dash==0.1.2   # pins gunicorn<22; see above
pip install -e .
python run.py          # docs + builder on :8054

# Test
python scripts/smoke_test.py       # 59 checks, no browser
python scripts/check_release.py    # version drift, stale bundle, packaging
pytest tests/

# Build a distribution
python -m build
```

The React sources in `src/lib/components/*.react.js` are the source of truth — the Python classes in `dash_email/` are generated from their PropTypes by `dash-generate-components`. The built bundle and wrappers are committed so git-based deploys (Render) work without a node toolchain.

**After editing `src/lib/components/*.react.js` you must run both `npm run build` and `npm run extract-meta`**, and commit the regenerated artifacts in the same commit — `check_release.py` compares git commit timestamps and flags a bundle older than its source.

The version lives in three files: `package.json` (which `setup.py` reads), `dash_email/package.json` (which `dash_email.__version__` reads, regenerated by `npm run extract-meta`), and `lib/constants.py`. `check_release.py` fails if they drift.

## Releasing

Tag-driven. `git tag -a vX.Y.Z && git push origin vX.Y.Z` runs [`release.yml`](.github/workflows/release.yml): it asserts the tag matches `package.json`, re-runs the consistency and smoke checks, builds, publishes to PyPI over **OIDC trusted publishing** (no API token stored anywhere), and opens a GitHub Release with that version's CHANGELOG section attached. A `workflow_dispatch` dry run publishes to TestPyPI instead.

Full runbook: [RELEASING.md](./RELEASING.md).

## Deployment

The documentation site runs at **[email.2plot.dev](https://email.2plot.dev)** on Render. The repo ships a `render.yaml` blueprint and `Dockerfile` — create a Render Blueprint from the repo, fill the `sync: false` secrets in the dashboard, point the `email.2plot.dev` CNAME at the service, and it auto-deploys on push to main with a `/healthz` health check.

The canonical origin lives in exactly one place — `DEFAULT_BASE_URL` in `lib/constants.py` (override per-environment with `DASH_EMAIL_BASE_URL`). `templates/index.html` carries `__CANONICAL_ORIGIN__` tokens that `run.py` substitutes at startup, so the canonical link, `og:url`, the JSON-LD, `sitemap.xml`, `robots.txt` and the llms.txt links cannot drift apart. Full runbook: [RELEASING.md](./RELEASING.md).

## Requirements

- Python >= 3.9  (the documentation site itself needs >= 3.10 — see below)
- Dash >= 4.1
- Node.js >= 18 — only to rebuild the JS bundle

The **package** needs only Python 3.9+ and Dash 4.1+; every combination in that range is
verified in CI. Running the **documentation site** from source additionally needs Python
3.10+, because `python-frontmatter` imports `typing.TypeGuard`. That floor does not apply
to `pip install dash-email`.

## Community & support

- 💬 [Discord](https://discord.gg/WEnZR35mrK) — questions and showcase
- ▶️ [YouTube @2plotai](https://www.youtube.com/channel/UC6Bmo0t0ZUpU_xKBYW0bJuQ) — tutorials
- 🐛 [GitHub Issues](https://github.com/pip-install-python/dash-email/issues) — bugs and feature requests

Come build with us.

## More from Pip Install Python LLC

dash-email is one of several tools built and maintained by **Pip Install Python LLC**:

| Project                                                          | What it is                                        |
|------------------------------------------------------------------|---------------------------------------------------|
| 📊 **[2plot.ai](https://2plot.ai)**                              | The network hub — data apps, analytics, sign-in   |
| 🎬 **[2plot.media](https://2plot.media)**                        | Videography application                           |
| 🧩 **[2plot.dev](https://2plot.dev)**                            | The full Dash component catalogue                 |
| 🤖 **[ai-agent.buzz](https://ai-agent.buzz)**                    | Infinite AI canvas                                |
| ⛵️ **[PiratesBargain](https://piratesbargain.com/shop)**         | E-commerce / digital commerce                     |

## License

MIT — see [LICENSE](LICENSE). dash-email is an independent wrapper inspired by [React Email](https://react.email)'s component patterns; emails you build with it are yours. Built by [Pip Install Python](https://github.com/pip-install-python).
