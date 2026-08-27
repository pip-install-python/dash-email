# Releasing — development to production

Three deliverables ship from this repo, and they are independent. You can do
them in any order, but this is the order that fails cheapest:

| # | Deliverable | Where | Rollback |
|---|---|---|---|
| 1 | Source | `github.com/pip-install-python/dash-email` | force-push the old ref |
| 2 | Package | `pypi.org/project/dash-email` | **none — a version is permanent** |
| 3 | Docs | `https://email.2plot.dev` (Render) | redeploy the previous commit |

The one irreversible step is PyPI. A filename can never be reused, even after
deletion, so a bad `0.2.0` costs you `0.2.1` forever. Everything below is
arranged so the irreversible step happens last, after the reversible ones have
already proven the artifact.

---

## Phase 0 — before anything leaves the machine

These are the checks nobody can do for you later.

```bash
# 1. Everything still boots, every page renders, every component survives
#    Dash's JSON encoder
python scripts/smoke_test.py                 # expect 59/59

# 2. Version consistency, packaging drift, stale bundle
python scripts/check_release.py --version 0.2.0

# 3. The support claim, actually measured
python scripts/compat_matrix.py              # writes COMPATIBILITY.md
```

**Status: done for 0.2.0.** The matrix has been run — 4.1.0 / 4.2.0 / 4.3.0 /
4.4.1 all pass 59/59. See [COMPATIBILITY.md](./COMPATIBILITY.md). `dash>=4.1`
is measured, not assumed; the previous `dash>=4.2.0` floor was never justified
by anything in the code.

Re-run the matrix for any release that touches `run.py`, `requirements.txt`, or
the component build.

### Two matrix modes

`compat_matrix.py` builds a throwaway virtualenv per Dash version and installs
the whole docs site into each. That needs network and a few GB of scratch
space, and it is the mode that catches a **dependency-resolution** conflict.

`compat_matrix.py --local` skips venv creation and runs the suite under
interpreters that already have each Dash installed, lending them this project's
site-packages for everything else:

```bash
python scripts/compat_matrix.py --local --search-root ~/PycharmProjects
```

That measures *our code against Dash X*, not *a fresh resolution against Dash
X* — the report says so in a banner. Use it offline; let CI do the clean leg.

### If you edited the components

`dash_email/*.py` and `dash_email/dash_email.min.js` are **generated and
committed**. After touching `src/lib/components/*.react.js`:

```bash
npm run build           # webpack bundle → dash_email/dash_email.min.js
npm run extract-meta    # PropTypes → dash_email/*.py + metadata.json
```

Commit the regenerated artifacts in the *same commit* as the source change.
`check_release.py` compares git commit timestamps (not mtimes — a fresh clone
has no meaningful mtimes) and flags a bundle older than `src/lib/components`.

---

## Phase 1 — GitHub

Push to `main`. CI runs on every push and PR:

- **`smoke`** — Dash 4.4.1 on the fleet Python 3.14 (the same minor the
  Dockerfile serves — `tests/test_python_version.py` pins the two together),
  plus 4.4.1 on the 3.13/3.12 window legs, plus the supported Dash range
  (4.1.0 / 4.2.0 / 4.3.0) on 3.12.
- **`package`** — `check_release.py`, `python -m build`, `twine check`, then
  the wheel installed into a clean venv with **only Dash present** and
  imported. That last part is what proves the package does not secretly need
  `requirements.txt`.
- **`package-python-range`** — the wheel imported and a full email layout built
  on Python 3.9 → 3.13, the exact range `python_requires` claims.
- **`lint-js`** — the committed bundle and `assets/*.js` parsed with node.

### One-time repo settings

- **Settings → Actions → General**: allow GitHub Actions.
- **Settings → Environments**: create an environment named `pypi`. Add yourself
  as a required reviewer if you want a manual gate between tag and upload.
- **Branch protection on `main`**: require the `CI` checks once the first run
  is green (you cannot select checks that have never run).

---

## Phase 2 — PyPI

### 2.1 Configure trusted publishing

No API token is stored anywhere. PyPI verifies a short-lived OIDC token minted
by GitHub for this exact repo + workflow + environment.

On **pypi.org → Your projects → dash-email → Publishing → Add a new publisher**:

| Field | Value |
|---|---|
| PyPI project name | `dash-email` |
| Owner | `pip-install-python` |
| Repository name | `dash-email` |
| Workflow name | `release.yml` |
| Environment name | `pypi` |

If the project does not exist on PyPI yet, use **Add a pending publisher**
instead — the first successful upload creates the project.

### 2.2 Dry run to TestPyPI

Do this before the real tag. Actions → Release → *Run workflow*, leave
`dry_run` checked. It builds, verifies and uploads to TestPyPI. Then install
from there into a clean venv:

```bash
python -m venv /tmp/tp && /tmp/tp/bin/pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  dash-email
/tmp/tp/bin/python -c "import dash_email as d; print(d.__version__, len(d.__all__))"
```

TestPyPI needs its own pending publisher (same form, on test.pypi.org).

### 2.3 Tag and publish

```bash
git tag -a v0.2.0 -m "dash-email 0.2.0 — Dash 4.1+ verified, CI/CD"
git push origin v0.2.0
```

`release.yml` then: asserts the tag matches `package.json`, re-runs
`check_release.py`, runs the smoke suite, builds, publishes via OIDC, and opens
a GitHub Release with this version's CHANGELOG section attached.

### 2.4 Manual fallback

If Actions is unavailable and you must publish from the machine:

```bash
python -m build
python -m twine check dist/*
python -m twine upload --config-file .claude/.pypirc dist/*
```

Prefer the workflow. A local upload skips every check the pipeline runs.

### 2.5 Verify

```bash
python -m venv /tmp/real && /tmp/real/bin/pip install dash-email
/tmp/real/bin/python -c "import dash_email as d; print(d.__version__)"
```

Check the PyPI page renders the README and the video thumbnail resolves.

---

## Phase 3 — email.2plot.dev

### 3.1 Create the service

Render dashboard → **New → Blueprint** → select the repo. `render.yaml`
declares the service, `/healthz` as the health check, the custom domain, and
every environment variable — secrets are marked `sync: false` for you to fill
in.

| Variable | What it unlocks | Missing → |
|---|---|---|
| `GOOGLE_API_KEY` | AI generation in `/email-builder` | builder runs in showcase mode |
| `RESEND_API_KEY` | sending and scheduling | send controls disabled |
| `CROSS_APP_WEBHOOK_SECRET` | 2plot.ai traffic reporting | hits ledger locally, nothing reported |
| `AD_SERVER_URL` / `AD_APP_ID` | 2plot.dev ad slots | slot stays hidden |
| `DASH_EMAIL_BASE_URL` | overrides the canonical origin | defaults to `https://email.2plot.dev` |

Every one of those is optional — the site boots and every documentation page
works with none of them set.

### 3.2 Custom domain

`render.yaml` declares `email.2plot.dev` on the service. Render will show a
target hostname; point the CNAME for `email` under `2plot.dev` at it, and
Render provisions the certificate once it resolves.

The `*.onrender.com` hostname keeps working and is **not** the canonical
origin. Every page advertises `email.2plot.dev` from the moment it deploys —
before DNS resolves, even — which is deliberate: it consolidates link equity on
the custom domain instead of splitting it across two hostnames.

The origin lives in exactly one place, `DEFAULT_BASE_URL` in
`lib/constants.py`. `templates/index.html` carries `__CANONICAL_ORIGIN__`
tokens that `run.py` substitutes at startup, so the canonical link, `og:url`,
the JSON-LD, `sitemap.xml`, `robots.txt` and the llms.txt links cannot disagree
with each other. `check_release.py` fails if a literal origin is ever pasted
back into the template, or if `render.yaml` stops serving the canonical host.

### 3.3 Register with the network — four places, each fails silently

1. **Hub satellite table** (`pip-docs+` repo, `lib/network_directory.py`) —
   flip this repo's `SATELLITES` entry from `status: "shipping"` to
   `"live"`, **in the same change that ships the site**. Until then
   `site_url()` resolves dash-email to its `legacy_url`
   (`dash-email-svmp.onrender.com`) and the hub keeps linking the old host.
   Do **not** reach for the global `SATELLITE_SUBDOMAINS_LIVE=1` flag — it
   promotes every `shipping` entry at once, including subdomains that do not
   resolve yet.
2. **Traffic hub health sweep** (2plot.ai env) — append to `PULSE_POLL_TARGETS`:
   `email=https://email.2plot.dev/healthz`
3. **Network directory** (2plotai `lib/network_directory.py`) — add the `email`
   key so `/traffic` labels the series instead of showing a bare slug.
4. **Ad network** — keys off `AD_APP_ID` (`dash-email`) separately.

Peer lists are the mirror image of this: **this repo must not advertise a
subdomain before it resolves**, and `scripts/smoke_test.py` fails if the two
known-NXDOMAIN hosts reappear in `lib/network_directory.py`. Re-verify with

```bash
curl -s https://email.2plot.dev/llms.txt | grep -oE 'https://[^ ]+/llms\.txt' | sort -u \
  | while read -r u; do printf "%s %s\n" "$(curl -s -o /dev/null -w '%{http_code}' "$u")" "$u"; done
```

Anything that is not `200` should come out of `PEERS` until it is.

### 3.4 Post-deploy checklist

1. `GET /healthz` → `{"status": "ok", "dash": "..."}`.
2. `/llms.txt`, `/robots.txt`, `/sitemap.xml` all 200, and every URL in them
   reads `https://email.2plot.dev` — not `*.onrender.com`.
3. View source on two pages and confirm each carries its **own** `<title>` and
   its **own** `<link rel="canonical">`. The smoke suite asserts this, but it
   asserts it against the test client, not against Render's proxy.
4. Open two component pages and confirm the email previews render in **both**
   light and dark mode. No automated check covers that end to end.
5. The demo video plays on the home page above *Features*.
6. `/email-builder` loads — with a key it generates, without one it shows the
   showcase.
7. `2plot.ai/traffic` grows an `email` series within one report interval.

---

## Cutting the next release

1. Land work on `main`; CI must be green.
2. Move `## [Unreleased]` content under a new `## [X.Y.Z] — <date>` heading.
3. Bump the version in **three** places — `package.json`,
   `dash_email/package.json`, `lib/constants.py`. `check_release.py` fails if
   they drift. (`setup.py` reads the root `package.json`, so it needs no edit;
   `dash_email/package.json` is what `dash_email.__version__` actually reads,
   and `npm run extract-meta` regenerates it from the root one.)
4. If any `.react.js` changed, `npm run build && npm run extract-meta` and
   commit the regenerated bundle and classes.
5. `python scripts/check_release.py --version X.Y.Z`
6. Tag `vX.Y.Z` and push. Everything else is automated.

## Known gaps

Worth doing, not blocking:

- **`tests/test_components.py` is thin.** It is import-and-smoke level, and
  three of its assertions test Python builtins rather than the library. The
  real coverage is `scripts/smoke_test.py`, which is integration-level.
- **No browser-level CI.** `compat_matrix.py --browser` exists and drives
  Playwright, but it is not wired into Actions — so "the bundle parses" is
  proven, "the components paint" is not.
- **No email-client rendering check.** Nothing verifies the exported HTML in
  Outlook or Gmail; that stays a manual pass through Litmus or equivalent.
- **The Dash matrix is Flask-only.** `--backends fastapi quart` works locally
  but is not in CI.
