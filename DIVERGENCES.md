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
   2.7.1-round wave-2 keep). RETIRED 2026-08-29 (sync item 13,
   1.6.35): the mechanism this entry described — hookless autoDeploy
   from `main`, the owner deliberately keeping
   `RENDER_DEPLOY_HOOK_URL` unset — is gone. cd.yml's `deploy` job
   now promotes a green `main` to `release` with a fast-forward
   `git push`, and render.yaml watches `release`; there is no hook
   step and no hook secret to leave unset. What survives from this
   entry: cd.yml's comment prose is still written from this repo's
   own seat rather than byte-copied from the template (see the new
   header comment and the per-step comments) — port template
   comment-level changes as contract, never as a byte-copy, for the
   same reason as before.

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

6. **No `yaml posture` fence — item 9 (1.6.30) is not adopted here.**
   Sync item 13 (1.6.35) asks for a `deploy: release-branch` key in
   this file's `yaml posture` fence; this fork has never carried that
   fence or its `tests/test_claude_kit.py` shape validator (`_POSTURE_KEYS`
   does not exist in this tree's kit test). Rather than fabricate a
   fence with one key and no validation behind it, the release-branch
   deploy road is recorded here in prose (divergence 2, retired
   2026-08-29) and in the `.claude/CLAUDE.md` kit trap instead. A
   verbatim item-13 port would add a fence CI never checks the shape
   of, which is exactly the silent-decay failure mode item 9 exists to
   prevent. Adopting item 9 properly (the fence + its validator) is a
   follow-up drop, not folded into this one.

7. **Item 16's navigation port keeps its own "App" sidebar category and
   drops one CSS-class pin the template's kwargs table no longer needs
   here.** `lib.constants.CATEGORY_ORDER` is
   `["Getting started", "App", "Components", "Templates"]` — "App"
   (the Email Builder, `pages/email_builder.py`'s
   `category="App", order=1`) is this fork's own identity category and
   must not be folded into "Components" per the sync spec's per-fork
   note; the template itself carries no such category. `UPSTREAM` is
   declared as React Email only (`https://react.email/docs`) — Resend
   is a sending integration the Email Builder uses, not something the
   documented COMPONENTS wrap, so it is not a second declared upstream
   (a link to Resend still lives on the builder's own page).
   `tests/test_nav_contract.py::test_code_blocks_cannot_widen_the_page`
   does NOT assert `table.m2d-block-kwargs` / `.m2d-block-props table`
   in `assets/main.css`: this repo's installed `markdown2dash` version
   renders `.. kwargs::` as a plain `dmc.Table` with no such class
   (`lib/directives/kwargs.py` delegates to the upstream `Kwargs`
   directive, which sets no `className`), so asserting the class would
   pin a selector nothing here ever emits. `table.m2d-table` (wide
   markdown tables) and the List/Blockquote/CodeHighlight overflow
   rules are ported verbatim. A verbatim template sync would fold
   Email Builder into "Components", add a second UPSTREAM entry, or
   reintroduce an untested CSS selector — port template changes to
   this area as contract, not as bytes.

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
