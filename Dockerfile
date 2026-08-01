# dash-email docs — production image (Render docker runtime).
#
# NO node toolchain: the dash_email component bundle + generated Python
# wrappers are COMMITTED to git (dash_email/*.min.js + *.py), and setup.py
# only reads package.json — so `pip install -e .` works without npm.
# TRADE-OFF: changes under src/lib/components require a local `npm run build`
# + `npm run extract-meta` and committing the regenerated artifacts.
FROM python:3.12-slim

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

# Render injects PORT and ignores EXPOSE; env vars (GOOGLE_API_KEY,
# RESEND_API_KEY) come from render.yaml / the dashboard — NEVER bake .env.
EXPOSE 8054

CMD ["sh", "-c", "gunicorn run:server --bind 0.0.0.0:${PORT:-8054} --workers ${WEB_WORKERS:-1} --timeout 120"]
