# dash-email docs — production image (Render docker runtime).
#
# NO node toolchain: the dash_email component bundle + generated Python
# wrappers are COMMITTED to git (dash_email/*.min.js + *.py), and setup.py
# only reads package.json — so `pip install -e .` works without npm.
# TRADE-OFF: changes under src/lib/components require a local `npm run build`
# + `npm run extract-meta` and committing the regenerated artifacts.
FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

# Render injects PORT and ignores EXPOSE; env vars (GOOGLE_API_KEY,
# RESEND_API_KEY) come from render.yaml / the dashboard — NEVER bake .env.
EXPOSE 8054

CMD ["sh", "-c", "gunicorn run:server --bind 0.0.0.0:${PORT:-8054} --workers ${WEB_WORKERS:-1} --timeout 120"]
