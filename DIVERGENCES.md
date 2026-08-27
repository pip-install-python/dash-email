# Divergences from the template

Every DELIBERATE difference between this repo and
dash-documentation-boilerplate, with its reason. This file is the
boundary between design and drift:

- Template syncs read this file FIRST and must not "restore" anything
  recorded here.
- A difference not recorded here is treated as drift and will be
  synced away.
- Record the divergence in the SAME commit that creates it — one
  line: what differs, why, and what the template would otherwise do.
- An empty list is a statement too: it means this repo intends to
  match the template exactly.

Fleet precedents for what belongs here: flexlayout's own-source
`_build_llms_doc` dedup and app-key sourcing; flows' own
`_health_body` payload shape (ports the healthz CONTRACT, not the
template's file); clerkhook's minimal `{ok, app, build}` healthz and
its heartbeat-as-before_request (the single anonymous 200 on a locked
host); muischeduler's no-npm dependabot scope.

## This repo's divergences

1. **Flask-only backend: the FastAPI healthz pin carries a second
   importorskip.** `tests/test_llms_routes.py`'s
   `test_fastapi_healthz_renders_from_the_shared_payload` adds
   `pytest.importorskip("lib.asgi_routes")` before the import,
   because this fork carries no `lib/asgi_routes.py` — the
   template's single-skip version ERRORS (instead of skipping) in
   any dev env that happens to have fastapi installed. The pin stays
   so a future backend port inherits it; requirements.txt keeps the
   `[fastapi]`/`[quart]` floor lines commented rather than active
   for the same reason. A verbatim sync would restore the
   single-importorskip form and break the suite here (recorded
   2026-08-24, the 2.7.1 floor round).

2. **cd.yml comment prose is written from this repo's seat** (the
   2.7.1-round wave-2 keep). The CONTRACT matches the template —
   build-match wait (`build == GITHUB_SHA`, 100 × 15s, job timeout
   30m), hookless ::warning, verify gated on both `cancelled` and
   `skipped` — but the header comment states that hookless
   autoDeploy is this service's deliberate deploy mechanism (the
   owner keeps `RENDER_DEPLOY_HOOK_URL` unset), the warning/wait
   comments tell the 2026-08-24 incident in this repo's words, and
   the verify comments name the social-card check this fork's
   smoke_live performs. A verbatim sync would replace the comments
   with the template's phrasing; port comment-level changes as
   contract instead.

3. **Dockerfile HEALTHCHECK probes with python-urllib, not curl.**
   This image apt-installs NOTHING — the component bundle is
   committed, so there is no node toolchain and no curl (the
   lean-image decision in the Dockerfile header). The template's
   probe is `curl -fsS`; ours is `python -c "…urllib…"` (clerkhook's
   shape) with the same `--interval/--timeout/--start-period/
   --retries` and the same `$PORT`-with-default contract
   (`os.environ.get('PORT','8054')` is the python spelling of
   `${PORT:-8054}`). A verbatim sync would reintroduce an apt layer
   for curl.

4. **scripts/smoke_live.py carries a fork-local network-bulletin check.**
   The file is the template's current copy (1.6.29 — wake loop, retry
   ladder, SSL context on both urlopens, head parity) plus one warn-only
   check in §4: "the network bulletin is wired", asserting the llms.txt
   viewer's "What's new" panel is not the "No announcements." fallback.
   Added after this host shipped live with `NETWORK_BULLETIN_URL` unset
   and nothing anywhere surfaced the empty panel (commit a28dd9b); two
   fork-owned tests in tests/test_smoke_live.py pin it (unwired warns,
   wired doesn't). The usage line in the docstring names this host. A
   byte-copy from the template would silently drop the check; port the
   template's future changes as contract around it (item 6's class since
   1.6.29 says exactly this).

5. **scripts/network_smoke.py is the fork-adapted battery, not the
   template's bytes.** Ours splits `fetch` into `fetch_raw` (bytes) +
   `fetch` (text) because the social-card real-pixels check reads the
   PNG IHDR dimensions from raw bytes — a lossy decode destroys the
   header — and carries the card checks (`social_card_real_pixels`,
   `installable_as_an_app`) plus a SAMPLE_PAGE constant the template
   does not have (the file's own header records the lineage: 1.2.4 +
   leaflet's card checks + the hub's real-pixels shape). Template
   battery changes port as CONTRACT: the 1.6.27
   `declared_python_minor`/`python_matches_declared` pair and the SSL
   context were ported that way, 2026-08-26. A verbatim sync would
   delete the card checks and break tests/test_network_smoke.py.

## Byte-owned paths

Paths this fork owns byte-for-byte. The F3b fan-out never overwrites
a path listed here; everything else in the spec's `sync-verbatim`
block is the template's to update mechanically. Prose above explains
divergences; this block is the machine answer.

Repo-relative paths, one per line, `#` comments, no `..`; exactly one
block. An EMPTY block means "the template owns every sync-verbatim
path here" — present so the absence is a statement. When the block
exists it is authoritative; a fork without it gets the conservative
mention heuristic (over-flags, never restores).

```yaml byte-owned
```
