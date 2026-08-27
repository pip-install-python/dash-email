# dash-email docs — production image (Render docker runtime).
#
# NO node toolchain: the dash_email component bundle + generated Python
# wrappers are COMMITTED to git (dash_email/*.min.js + *.py), and setup.py
# only reads package.json — so `pip install -e .` works without npm.
# TRADE-OFF: changes under src/lib/components require a local `npm run build`
# + `npm run extract-meta` and committing the regenerated artifacts.
# The fleet Python (sync item 5, template 1.6.27): MINOR tag only, never a
# patch pin — `3.X.Y-slim` stops receiving 3.X fix releases the day it is
# written down, while the minor tag tracks them through the registry.
# tests/test_python_version.py holds the CI site lane and cd.yml's verify to
# this same minor; /healthz's `python` field + the battery's
# python_matches_declared check hold the serving host to it.
FROM python:3.14-slim

WORKDIR /app

# Without this, NONE of the app's boot diagnostics reach the platform's log
# stream. Python block-buffers stdout when it is a pipe rather than a TTY, and
# gunicorn never flushes it — so "[dash-email] Starting Dash 4.4.1", the
# satellite-reporter state line, and the network-bulletin wired/off line all
# sat in a buffer while Render's log view showed only gunicorn's own output.
#
# That is not cosmetic. The bulletin line exists precisely so you can tell at a
# glance which of the two states a deployment is in, and its absence is how
# email.2plot.dev shipped with NETWORK_BULLETIN_URL unset — the viewer rendered
# an empty "What's new" panel and the one log line that would have said so was
# never printed.
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip

# vendor/ holds dash_clerk_auth (not on PyPI), which requirements.txt installs
# from this path — so vendor/ MUST be copied before the requirements install
# (emojimart's image died on the reverse order, and pip reports the missing
# path as a SOFT warning before an OSError that reads like a registry
# outage). Auth stays gated at runtime: no CLERK_* keys, no login wall.
#
# CACHE SEMANTICS (the round-2 fleet lesson, found by pannellum
# 2026-08-22): this layer re-runs ONLY when vendor/ or requirements.txt
# bytes change. A `>=` floor can NEVER pull a newer release through a
# cache hit — a code-only commit rebuilds the app layers below while pip
# silently keeps whatever version the image was first built with. Ship
# every dependency upgrade as a floor bump in requirements.txt (grep the
# number — it also lives in run.py's boot floor and the tests): the bump
# IS the cache bust, and the boot floor turns a stale image from a
# silent downgrade into a loud refusal to start.
COPY vendor/ ./vendor/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# markdown2dash pins gunicorn<22, conflicting with the CVE-driven gunicorn>=23
# in requirements.txt (CVE-2024-6827, CVE-2024-1135 — request smuggling). Its
# real dependencies are all in requirements.txt already, so it is installed
# alone, without letting pip see the spurious pin. CI asserts the resulting
# gunicorn version inside this image, which is what keeps the dodge honest.
RUN pip install --no-cache-dir --no-deps markdown2dash==0.1.2

COPY . .
RUN pip install --no-cache-dir -e .

# Docker's own health verdict — what an orchestrator relying on container
# health reads, and what CI's "Assert Docker's own health verdict" step
# polls (a broken probe ships silently while every EXTERNAL curl stays
# green — emojimart's F2 finding, 2026-08-24). The template probes with
# curl; this image apt-installs NOTHING (committed JS bundle, no node, no
# curl — see the header), so the probe is python-urllib instead
# (clerkhook's shape; recorded in DIVERGENCES.md). Same variable, same
# default as the CMD bind below: a probe on a hardcoded port goes
# unhealthy the day the platform moves the bind.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import os,urllib.request;urllib.request.urlopen('http://localhost:'+os.environ.get('PORT','8054')+'/healthz',timeout=4)" || exit 1

# Render injects PORT and ignores EXPOSE; env vars (GOOGLE_API_KEY,
# RESEND_API_KEY) come from render.yaml / the dashboard — NEVER bake .env.
EXPOSE 8054

CMD ["sh", "-c", "gunicorn run:server --bind 0.0.0.0:${PORT:-8054} --workers ${WEB_WORKERS:-1} --timeout 120"]
