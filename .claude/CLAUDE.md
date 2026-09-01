# Claude Code Project Guide - Dash Email

## Project Overview

**dash-email** is a Plotly Dash component library that wraps [React Email](https://react.email) components, enabling developers to build and preview email templates directly within Dash applications.

This project bridges the gap between Dash's Python-first approach and React Email's powerful email component system, allowing developers to:
- Design email templates using familiar Dash patterns
- Preview emails in real-time within a Dash app
- Export email templates as HTML for sending via any email service

The repo is two things at once: the `dash_email` component package
(`src/` → committed build artifacts in `dash_email/`) and its
documentation site, https://email.2plot.dev, served by `run.py` — a fork
of dash-documentation-boilerplate (see the network section at the end of
this file). `python run.py` runs the docs site; `python usage.py` is the
minimal component demo.

---

## Technology Stack

### Core Framework
- **Python 3.9+** - Required runtime
- **Dash 4.x** - Primary web framework (floor 4.1; CI's matrix tests 4.1 → current)
- **React 18.x** - Frontend runtime

### React Email Integration
- **@react-email/components** - Core email components
- **@react-email/render** - HTML rendering utility

### Build Tools
- **Node.js 18+** - Required for component development
- **Webpack 5** - Module bundler
- **Babel** - JavaScript transpiler

---

## Quick Start

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install JavaScript dependencies
npm install

# Build the component
npm run build

# Run the demo app
python usage.py
```

---

## Resources

- **React Email Docs**: https://react.email/docs
- **React Email Components**: https://react.email/docs/components/html
- **Dash Component Boilerplate**: https://github.com/plotly/dash-component-boilerplate
- **Dash Documentation**: https://dash.plotly.com
- **Pip Install Python**: https://pip-install-python.com

---

## Component Architecture

### React Email Components to Wrap

| React Email | Dash Component | Purpose |
|-------------|----------------|---------|
| `Html` | `Email` | Root wrapper for email templates |
| `Head` | `EmailHead` | Email metadata (title, styles) |
| `Preview` | `EmailPreview` | Preview text in inbox |
| `Body` | `EmailBody` | Email body wrapper |
| `Container` | `EmailContainer` | Centered content container |
| `Section` | `EmailSection` | Grouping sections |
| `Row` | `EmailRow` | Horizontal row |
| `Column` | `EmailColumn` | Column within row |
| `Button` | `EmailButton` | Call-to-action button |
| `Link` | `EmailLink` | Hyperlink |
| `Text` | `EmailText` | Paragraph text |
| `Heading` | `EmailHeading` | H1-H6 headings |
| `Img` | `EmailImage` | Image component |
| `Hr` | `EmailDivider` | Horizontal divider |
| `Tailwind` | `EmailTailwind` | Tailwind CSS support |
| `Markdown` | `EmailMarkdown` | Markdown rendering |
| `CodeBlock` | `EmailCodeBlock` | Code syntax highlighting |
| `CodeInline` | `EmailCodeInline` | Inline code |
| `Font` | `EmailFont` | Custom font loading |

---

## Agent Reference

| Agent | Domain | When to Use |
|-------|--------|-------------|
| `react-component-dev` | React/JSX | Building React components |
| `dash-integration` | Dash/Python | Python API, callbacks |
| `email-specialist` | React Email | Email-specific patterns |
| `build-tools` | Webpack/npm | Build configuration |

See `.claude/agents/` for full agent configurations.

---

## Development Workflow

1. **Component Development**: Write React components in `src/lib/components/`
2. **Build**: Run `npm run build` to compile
3. **Python API**: Auto-generated in `dash_email/`
4. **Testing**: Use `usage.py` for visual testing
5. **Publish**: Build and publish to PyPI/npm

---

## Network role & the behavioral contract

This repo is a member of the 2plot network — either the template
itself (dash-documentation-boilerplate) or a fork of it serving one
component's documentation. **Identity derives from the repo, never
from this file**: the app key comes from `SATELLITE_APP_KEY` and
run.py's fork point, the host from `lib/constants.py`'s `BASE_URL`,
the deliberate differences from the template from `DIVERGENCES.md`
at the repo root. If those disagree with anything written here,
they win.

### The contract — every session, every prompt

1. **Check the prompt against this tree before executing.** Prompts
   are written from the template's perspective and your fork may
   legitimately differ — floors, backends, payload shapes, page
   sets. A prompt step that doesn't fit this repo is a finding to
   return, not an instruction to force.
2. **Corrections are your job, not scope creep.** If a prompt's
   reference list doesn't match its steps, if its assumed state is
   wrong, or if executing it as written would produce a
   green-but-vacuous result, say so and propose the corrected
   version before running it.
3. **Verify your own deploy on the wire before reporting.** A push
   is not a result. Run `/wire-verify` (or its manual equivalent)
   against production and paste what came back. If your sandbox
   cannot reach your own domain, say exactly that — an unverified
   claim marked as unverified is honest; the same claim unmarked is
   not.
4. **Report observed versus expected, with evidence.** Paste the
   JSON, the status code, the test count. "Should work" and summary
   claims without artifacts are not reports.
5. **Divergence is legitimate when written down.** Before syncing
   template changes, read `DIVERGENCES.md`; never let a sync
   "restore" a recorded deliberate difference. When you deliberately
   diverge, record it there in the same commit — an unrecorded
   divergence is indistinguishable from drift and will be treated
   as drift.
6. **Never touch**: environment variable VALUES, hosting dashboards,
   secrets, other repos' trees, or anything the prompt didn't put in
   scope. Enumerate what you cannot do (closing PRs, dashboard
   steps) for the owner instead of claiming it done.

### Verification traps (fleet-learned, keep them)

- A `>=` floor can never pull a new release through a Docker cache
  hit — the requirements line changing IS the cache bust, and floors
  live in several encodings (requirements, run.py's boot floor,
  tests, CI): grep the number, move every one.
- `/healthz` build == HEAD is the deploy proof; a missing geo block
  on dimll ≥2.7 means the cache trap fired (unless DIVERGENCES.md
  says this host's healthz is deliberately minimal).
- Probe with GET, not HEAD — HEAD responses omit the Link headers.
- Run-watchers keyed on a commit sha can match Dependabot's runs on
  the same sha — key on the workflow path (cd.yml) instead.
- The browser lane and the machine lane are different documents;
  a fix proven on one is unproven on the other.
- `build == HEAD` on `/healthz` means HEAD of **`release`**, not main
  (sync item 13, 1.6.35). Render deploys `release`; only cd.yml's
  `deploy` job writes it, fast-forward, after the CI matrix is green.
  `main` ahead of `release` is an uncertified push pending — its CD
  run is red or still running — never "drift" and never a reason to
  deploy by hand or to write `release` yourself (a non-fast-forward
  push fails the next run on purpose). Compare the wire against
  `git rev-parse origin/release`. DIVERGENCES.md's posture fence
  declares `deploy: release-branch` — but that names the CODE road,
  not the platform's live state: until the Render dashboard's Branch
  field is flipped to `release` (an owner step this session never
  takes), Render may still be deploying `main` directly. Check which
  by comparing `/healthz` build against `origin/main` vs
  `origin/release` after a push where they'd diverge.
- There is ONE classifier: `dash_improve_my_llms.classify()`. Never
  add a User-Agent list to this app — the tracker had one for a year
  (`lib/analytics_tracker.py`, until sync item 12), it filed ClaudeBot
  as *search* (it is Anthropic's training crawler; the package's
  registry says so), it still named the retired `anthropic-ai` /
  `claude-web` tokens, and it counted every UA-less or library client
  as a human. A token the registry lacks is a pushback to the package
  seat, not a list here; `tests/test_analytics_classifier.py` greps
  the module for the old tokens and goes red if one comes back.
- Item 16's kwargs-table CSS class (`table.m2d-block-kwargs` /
  `.m2d-block-props table`) does not apply to this fork —
  `lib/directives/kwargs.py` delegates to an older `markdown2dash`
  `Kwargs` directive that stamps no class on its `dmc.Table`. Don't
  let a future sync "restore" that selector into `assets/main.css`
  or its test assertion; see DIVERGENCES.md entry 7.
- Which branch Render actually builds can be measured on a GREEN push,
  by TIMING, without waiting for a red one (leaflet, 2026-08-31 — the
  method, not just its answer). `main == release == wire` at every step
  of a promote tells you nothing: both refs hold the same sha, so the
  wire cannot separate them, and four promotes across three hosts said
  nothing at all. Sample `/healthz` every ~45 s from the moment of the
  push and note when the swap lands relative to the PROMOTE, not the
  push. leaflet measured build+swap at 2m03s from the promote; had
  Render reacted to the push instead, the same 2m03s would have put the
  build live ~1m52s earlier than it appeared, and the wire was still
  serving the old sha well past that point. That is STRONG EVIDENCE
  that Render is building `release` — not proof, since a queued or slow
  build could in principle produce the same shape. The canonical
  discriminator is unchanged and still owed: the first push that goes
  RED on main must leave `release` unmoved and the wire unchanged.
  Worth taking on every SECOND promote — it costs one background
  sampler and converts "asserted" into "strongly evidenced".
- Verify the artifact the claim is about, and say which one you
  measured. Three hosts got this wrong in one round while holding the
  rule: a skip link checked in the received HTML lives in the RENDERED
  DOM (muicharts, twice inside an hour, having written the rule
  itself); a props table absent from the crawler document is a defect
  of the site, not of the harness — pannellum moved that assertion onto
  the rendered layout and the pin passed for a fortnight over a corpus
  serving zero props. WHEN A LANE DISAGREES, THAT IS THE FINDING; never
  relocate the assertion to the lane that passes. And an owner-gated
  section needs BOTH cookie states to be a measurement at all
  (modelviewer: `credentials: 'include'` → 2,962 B with admin hrefs,
  `'omit'` → 108 B with none — hidden, not merely styled away).
  The error runs BOTH ways and the second one is worse, because it
  sends someone hunting a bug that does not exist: `curl https://…/ |
  grep -c skip-link` returns **0** on a host where the skip link is
  shipped and working (excalidraw, 2026-08-31) — it is a Dash
  component in `app.layout`, so React renders it and the served HTML
  never contains it. A fork "verifying the skip link on the wire" with
  curl reports a missing feature that is present. Anything built by
  the layout rather than written into the template is invisible to the
  two artifacts curl can reach; assert it through the layout or a real
  browser, and say which you used.
- Assert the corpus is NON-EMPTY before trusting any negative, and print
  the count beside the result (note 88). A sweep that found nothing and a
  sweep that swept nothing produce the same green, and only one of them
  is evidence. Measured on the template, 2026-09-01: its `.flake8` excludes
  `docs/*/`, so `flake8 docs/` exits 0 with a file in `docs/` containing
  `def broken(:` — the linter is not passing that file, it is not reading
  it; `py_compile` sees it at once. Same family, same day: a naive
  substring count read fenced documentation as defects, a file-scoped grep
  matched prose ABOUT the defect it was hunting, a `git show … && diff`
  printed "(empty = same)" on a comparison that never ran, and `pytest … |
  tail -2 && git commit` committed over a red suite because a pipeline's
  exit status is the LAST command's. Capture the exit code; count what you
  swept; say both.
- And the same family one turn later, worth keeping because it nearly
  shipped a wrong fact into a spec: extracting a package constant with
  `re.search(r"EVENT_FIELDS = \((.*?)\)", src, re.S)` truncated at a `)`
  inside a COMMENT in the middle of the tuple, printed eight of sixteen
  fields, and reported `'ua' present: False` — confidently, with a
  number beside it. Caught only because eight looked too few. When you
  parse a language construct out of source with a regex, check the count
  against something independent (the file, `python -c "from … import X;
  print(len(X))"`, the CHANGELOG) before you believe a negative.