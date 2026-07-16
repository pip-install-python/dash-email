<div align="center">

# Dash Email

**Email components for [Plotly Dash](https://dash.plotly.com), wrapping [React Email](https://react.email) patterns.**

15 email-safe components · table-based layouts · AI-powered builder · live preview · send via Resend · full Dash callback interoperability.

[![PyPI version](https://img.shields.io/pypi/v/dash-email?color=blue)](https://pypi.org/project/dash-email/)
[![Python](https://img.shields.io/pypi/pyversions/dash-email)](https://pypi.org/project/dash-email/)
[![Dash 4.2+](https://img.shields.io/badge/Dash-4.2%2B-1a1a2e?logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white)](https://discord.gg/WEnZR35mrK)
[![YouTube](https://img.shields.io/badge/YouTube-%402plotai-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/channel/UC6Bmo0t0ZUpU_xKBYW0bJuQ)

**[Documentation](https://pip-install-python.com)** · [Discord](https://discord.gg/WEnZR35mrK) · [YouTube](https://www.youtube.com/channel/UC6Bmo0t0ZUpU_xKBYW0bJuQ) · [GitHub](https://github.com/pip-install-python/dash-email)

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

> ⚠️ dash-email is in early release (0.0.x). The component API is stable, but the AI builder and sending utilities are actively evolving.

## Installation

```bash
pip install dash-email
```

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

### 📚 **[pip-install-python.com](https://pip-install-python.com)**

Run the full documentation site — component pages with isolated live examples, props tables, and the AI email builder — locally:

```bash
git clone https://github.com/pip-install-python/dash-email.git
cd dash-email
pip install -r requirements.txt
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
pip install -e .
python run.py          # docs + builder on :8054
```

The React sources in `src/lib/components/*.react.js` are the source of truth — the Python classes in `dash_email/` are generated from their PropTypes by `dash-generate-components`. The built bundle and wrappers are committed so git-based deploys (Render) work without a node toolchain.

## Deployment

The repo ships a `render.yaml` blueprint and `Dockerfile` — create a Render Blueprint from the repo, fill the `sync: false` secrets in the dashboard, and it auto-deploys on push to main with a `/healthz` health check.

## Requirements

- Python >= 3.9
- Dash >= 4.2.0
- Node.js >= 18 (only for building components from source)

## Community & support

- 💬 [Discord](https://discord.gg/WEnZR35mrK) — questions and showcase
- ▶️ [YouTube @2plotai](https://www.youtube.com/channel/UC6Bmo0t0ZUpU_xKBYW0bJuQ) — tutorials
- 🐛 [GitHub Issues](https://github.com/pip-install-python/dash-email/issues) — bugs and feature requests

Come build with us.

## More from Pip Install Python LLC

| Project                                             | What it is                        |
|-----------------------------------------------------|-----------------------------------|
| 🧩 **[Component Library](https://2plot.dev)**       | The full Dash component catalogue |
| ⛵️ **[piratesbargain](https://piratesbargain.com)** | E-commerce tool focused app       |
| 🤖 **[ai-agent.buzz](https://ai-agent.buzz)**       | ai canvas / bucket tool           |

## License

MIT — see [LICENSE](LICENSE). dash-email is an independent wrapper inspired by [React Email](https://react.email)'s component patterns; emails you build with it are yours. Built by [Pip Install Python](https://github.com/pip-install-python).
