#!/usr/bin/env python
"""Pre-release consistency check for dash-email.

Run this before cutting a tag. It catches the release-shaped mistakes that no
functional test can see, because the app runs perfectly with all of them:

1. **Version drift across three files.** `setup.py` reads the version straight
   out of the **root** `package.json`, so that is what PyPI serves. But
   `dash_email.__version__` is read at import time from
   `dash_email/package.json`, which is a *different* file — it is regenerated
   by `npm run extract-meta` from the root one. Bump the root and forget the
   rebuild and you ship a wheel labelled 0.2.0 whose `__version__` says 0.0.1.
   `lib/constants.py` is the third: it is what the docs site shows.
2. **The built bundle missing or stale** relative to the React source.
3. **CHANGELOG not mentioning the version being released.**
4. **Packaging drift** — the wheel picking up more than `dash_email/`, or the
   Dash floor in `setup.py` disagreeing with what CI actually tests.

    python scripts/check_release.py                   # check
    python scripts/check_release.py --version 0.2.0   # also assert the target

Exit code 0 when clean, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The Dash floor this project promises. CI's matrix starts here; setup.py must
# agree, or the promise and the measurement have quietly diverged.
DASH_FLOOR = "4.1"

problems: list[str] = []
notes: list[str] = []


def strip_html_comments(html: str) -> str:
    """`<!-- ... -->` removed, so a check cannot match its own explanation.

    templates/index.html documents at length *why* it no longer hard-codes a
    canonical — quoting the tag it must not contain. Matching raw text made
    the check fail on the very comment describing the fix.
    """
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def strip_python_comments(source: str) -> str:
    """Comments and docstrings removed — same trap, other language.

    run.py explains the retired canonical shim and the deleted OAI-SearchBot
    workaround by name. Grepping the file for those names finds the prose.
    """
    import io
    import tokenize

    out = []
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except tokenize.TokenError:
        return source
    prev_type = tokenize.INDENT
    for tok in toks:
        if tok.type == tokenize.COMMENT:
            continue
        # A STRING alone on a logical line is a docstring, not a value.
        if tok.type == tokenize.STRING and prev_type in (
            tokenize.INDENT, tokenize.NEWLINE, tokenize.NL, tokenize.DEDENT,
        ):
            continue
        out.append(tok.string)
        if tok.type not in (tokenize.NL, tokenize.NEWLINE):
            prev_type = tok.type
        else:
            prev_type = tok.type
    return " ".join(out)


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"  {'PASS' if ok else 'FAIL'}  {label:<46} {detail}")
    if not ok:
        problems.append(f"{label}: {detail}")


def check_bundle_freshness(bundle: Path) -> None:
    """Is the committed JS bundle older than the React source it is built from?

    This deliberately does NOT compare filesystem mtimes. Git does not record
    them, so a fresh clone stamps every file with its checkout time and the
    comparison is decided by sub-second write ordering — which would make this
    check fail at random in CI while passing on the machine that built the
    bundle.

    Git commit timestamps are the stable signal, and they answer the question
    that actually matters: did someone edit a .react.js and commit without
    running `npm run build`? Rebuilding and committing together puts both in
    the same commit, so equal timestamps are the healthy case.
    """
    def last_commit(path: str) -> int | None:
        try:
            out = subprocess.run(
                ["git", "log", "-1", "--format=%ct", "--", path],
                cwd=ROOT, capture_output=True, text=True, timeout=15,
            )
            return int(out.stdout.strip()) if out.stdout.strip() else None
        except Exception:  # noqa: BLE001 — not a git checkout, or no git
            return None

    bundle_at = last_commit(str(bundle.relative_to(ROOT)))
    src_at = last_commit("src/lib/components")

    if bundle_at is None or src_at is None:
        notes.append(
            "bundle freshness not checked — no git history here (a tarball "
            "install, or a shallow clone without the relevant commits)."
        )
        print(f"  SKIP  {'bundle newer than src/lib/components':<46} no git history")
        return

    check("bundle newer than src/lib/components", bundle_at >= src_at,
          "up to date" if bundle_at >= src_at else
          f"STALE — src committed {src_at - bundle_at}s after the bundle; "
          "run npm run build && npm run extract-meta and commit the result")


def versions() -> dict[str, str]:
    out: dict[str, str] = {}
    out["package.json (setup.py reads this)"] = json.loads(
        (ROOT / "package.json").read_text()
    )["version"]
    shipped = ROOT / "dash_email" / "package.json"
    if shipped.exists():
        out["dash_email/package.json (__version__)"] = json.loads(
            shipped.read_text()
        )["version"]
    out["lib/constants.py APP_VERSION"] = re.search(
        r'^APP_VERSION\s*=\s*"([^"]+)"', (ROOT / "lib" / "constants.py").read_text(), re.M
    ).group(1)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", help="assert every source reports this version")
    args = ap.parse_args()

    print("\ndash-email release check\n" + "=" * 62)

    print("\n[versions]")
    vs = versions()
    for name, v in vs.items():
        print(f"        {name:<46} {v}")
    unique = set(vs.values())
    check("all version sources agree", len(unique) == 1,
          "consistent" if len(unique) == 1 else f"differ: {sorted(unique)}")
    target = args.version or vs["package.json (setup.py reads this)"]
    if args.version:
        check(f"every source is {args.version}", unique == {args.version},
              "ok" if unique == {args.version} else f"found {sorted(unique)}")

    print("\n[build artifacts]")
    bundle = ROOT / "dash_email" / "dash_email.min.js"
    check("JS bundle committed", bundle.exists(),
          f"{bundle.stat().st_size // 1024} KB" if bundle.exists()
          else "MISSING — run npm run build")
    if bundle.exists():
        check_bundle_freshness(bundle)

    generated = sorted(p.stem for p in (ROOT / "dash_email").glob("Email*.py"))
    react = sorted(p.name.replace(".react.js", "")
                   for p in (ROOT / "src" / "lib" / "components").glob("*.react.js"))
    check("a Python class per React component",
          set(generated) == set(react),
          f"{len(generated)} classes"
          if set(generated) == set(react)
          else f"drift: {sorted(set(react) ^ set(generated))} — run npm run extract-meta")

    print("\n[changelog]")
    changelog_path = ROOT / "CHANGELOG.md"
    if changelog_path.exists():
        changelog = changelog_path.read_text()
        check(f"CHANGELOG mentions {target}", target in changelog,
              "found" if target in changelog else f"add a [{target}] section")
        if "## [Unreleased]" in changelog:
            body = changelog.split("## [Unreleased]", 1)[1].split("## [", 1)[0]
            if body.strip() and "Nothing yet" not in body:
                notes.append(
                    "CHANGELOG still has content under [Unreleased] — move it under "
                    f"[{target}] before tagging."
                )
    else:
        check("CHANGELOG.md present", False, "MISSING")

    print("\n[packaging]")
    setup_py = (ROOT / "setup.py").read_text()
    check("only dash_email is packaged",
          'packages=["dash_email"]' in setup_py.replace("'", '"'),
          "docs/, pages/ and lib/ stay out of the wheel")
    floor = re.search(r'"dash>=([\d.]+)"', setup_py)
    check(f"setup.py Dash floor is {DASH_FLOOR}",
          floor is not None and floor.group(1).startswith(DASH_FLOOR),
          f"dash>={floor.group(1)}" if floor else "no dash requirement found")
    check("dash is the only hard runtime dependency",
          re.search(r'install_requires=\[\s*"dash>=[\d.]+",?\s*\]', setup_py) is not None,
          "docs + builder deps live in extras / requirements.txt")
    check("LICENSE present", (ROOT / "LICENSE").exists())
    check("README present", (ROOT / "README.md").exists())
    check("MANIFEST.in present", (ROOT / "MANIFEST.in").exists())

    print("\n[seo]")
    # templates/index.html hard-codes the canonical origin (it has to — it is a
    # static file). Everything else absolute — sitemap.xml, robots.txt, the
    # llms.txt URLs, the server-injected canonical — is generated from
    # DOCS_BASE_URL. If those two drift, half the site points at one hostname
    # and half at another, which is the split-signal version of having no
    # canonical at all.
    tpl = (ROOT / "templates" / "index.html").read_text()
    base = re.search(
        r'^DEFAULT_BASE_URL\s*=\s*"([^"]+)"', (ROOT / "lib" / "constants.py").read_text(), re.M
    ).group(1).rstrip("/")
    check("template takes its origin from constants.py",
          "__CANONICAL_ORIGIN__" in tpl,
          f"{tpl.count('__CANONICAL_ORIGIN__')} tokens → {base}")
    # A literal origin left in the template is the drift this design removes.
    hard_coded = sorted(set(re.findall(r"https://[a-z0-9.-]*(?:onrender\.com|2plot\.dev)", tpl)))
    check("no hard-coded origin left in the template", not hard_coded,
          "all tokenised" if not hard_coded else "found: " + ", ".join(hard_coded))
    # The deployed origin and the blueprint must agree, or the canonical points
    # somewhere Render is not serving.
    render_yaml = (ROOT / "render.yaml").read_text()
    host = base.split("://", 1)[-1]
    check("render.yaml serves the canonical host", f"- {host}" in render_yaml,
          f"domains: {host}")
    # dash-improve-my-llms >= 2.3.3 prerenders <link rel="canonical"> per route.
    # A literal tag in the template would be a SECOND canonical on every page,
    # and two canonicals is worse than none — engines may discard both. The
    # `<` is what distinguishes a real tag from the querySelector string the
    # client-side sync script legitimately contains.
    tpl_markup = strip_html_comments(tpl)
    check("template hard-codes no canonical",
          '<link rel="canonical"' not in tpl_markup,
          "the package prerenders it per route")
    check("retired canonical placeholder is gone",
          "<!--CANONICAL-->" not in tpl,
          "no dead markup from the 2.0-era shim")
    run_py = (ROOT / "run.py").read_text()
    run_code = strip_python_comments(run_py)
    # strip_python_comments re-joins tokens with spaces, so `a.b(` comes back
    # as `a . b (`. Structural checks match against the whitespace-free form.
    run_dense = re.sub(r"\s+", "", run_code)
    check("run.py does not re-add a canonical shim",
          'rel="canonical"' not in run_code,
          "interpolate_index override retired at 2.3.3")
    # A static duplicate of anything register_page() emits is strictly worse
    # than the per-page tag, because engines choose between duplicates blind.
    head = tpl.split("</head>")[0]
    restated = [t for t in ('name="description"', 'property="og:title"',
                            'property="og:description"', 'property="og:type"',
                            'name="twitter:card"', 'name="twitter:title"',
                            'name="twitter:description"')
                if t in head]
    check("template does not restate per-page meta tags", not restated,
          "only site-level tags" if not restated else "duplicates Dash: " + ", ".join(restated))

    print("\n[network]")
    reqs_txt = (ROOT / "requirements.txt").read_text()
    floor = re.search(r"dash-improve-my-llms\[flask\]>=([\d.]+)", reqs_txt)
    ok_floor = floor is not None and tuple(
        int(x) for x in floor.group(1).split(".")
    ) >= (2, 3, 3)
    check("dash-improve-my-llms floor >= 2.3.3", ok_floor,
          f">={floor.group(1)}" if floor else "not pinned in requirements.txt")
    check("no leftover OAI-SearchBot workaround",
          "OAI-SearchBot" not in run_code,
          "fixed upstream in 2.3.2")
    check("network directory wired",
          "network_directory.apply(" in run_dense,
          "register_network before add_llms_routes")
    for mod in ("network_directory", "analytics_tracker",
                "traffic_rollup", "satellite_reporter"):
        check(f"lib/{mod}.py present", (ROOT / "lib" / f"{mod}.py").exists())
    check("hand-rolled traffic_reporter removed",
          not (ROOT / "lib" / "traffic_reporter.py").exists(),
          "replaced by the boilerplate analytics chain")

    print("\n[docs site]")
    for f in ("Dockerfile", "render.yaml", "requirements.txt", "run.py"):
        check(f"{f} present", (ROOT / f).exists())
    reqs = (ROOT / "requirements.txt").read_text()
    check("requirements use no absolute paths", "file:///" not in reqs,
          "no absolute file:// URLs")
    check("requirements tag the Dash line for the matrix",
          "# COMPAT-MATRIX: dash" in reqs,
          "compat_matrix.py strips it per run")

    print("\n[ci]")
    for wf in ("ci.yml", "release.yml"):
        check(f".github/workflows/{wf}", (ROOT / ".github" / "workflows" / wf).exists())

    print("\n" + "=" * 62)
    for n in notes:
        print(f"NOTE: {n}")
    if problems:
        print(f"\n{len(problems)} problem(s) — not ready to tag:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nClean. Ready to tag "
          f"v{target} (see RELEASING.md for the rest of the runbook).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
