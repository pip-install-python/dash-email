"""One fleet Python — image, matrix and render.yaml must agree.

Found by the ops seat reading the tree, not a report (2026-08-25): the
template's Dockerfile said `python:3.11.8-slim` — a PATCH pin, so the image
never received a 3.11.x security release — while the CI matrix said 3.12 and
render.yaml said 3.12.0. Three declared Pythons, the docker boot/battery
testing an interpreter the matrix never ran, and nothing on the wire able to
contradict any of them. These pins hold every encoding to ONE minor, sourced
from the Dockerfile's FROM tag; /healthz's `python` field plus the
`python_matches_declared` battery check (scripts/network_smoke.py) hold the
serving host to the same one.

What is deliberately NOT here: no comparison of the RUNNING interpreter to
the fleet minor — the suite legitimately runs on the adjacent window legs
(the matrix's 3.13/3.12 rows), where that assertion would be false by
design. Image-vs-declaration is the battery's job, against a host.

TWO Pythons live in this repo's ci.yml, and this file pins only one of them
(1.6.28 — filed independently by flows and clerkhook): the SITE lane — the
jobs that install requirements.txt and boot/serve the docs app — is held to
the image's minor. The PACKAGE lane (the `package` and
`package-python-range` jobs, testing the dash_email wheel's
`python_requires` claim of 3.9+) is the package's business and out of
scope; pinning it to a container base would fail the moment the image
moved. SITE_LANE_JOBS below is the explicit boundary between the two, so
the two Pythons are never conflated — adding a site-lane job to ci.yml
means adding its name there in the same change.
"""
from __future__ import annotations

import re

from conftest import REPO_ROOT

# The jobs that install requirements.txt and boot/serve the DOCS SITE.
# Everything else in ci.yml (package, package-python-range, lint-js) belongs
# to the dash_email package and is exempt from the fleet pin.
SITE_LANE_JOBS = {"lint", "docs-tests", "smoke", "docker", "pip-audit"}


def _fleet_minor() -> str:
    """The single source: the Dockerfile's FROM tag."""
    for line in (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8").splitlines():
        m = re.match(r"FROM\s+python:(\S+)", line)
        if m:
            return m.group(1)
    raise AssertionError("Dockerfile has no `FROM python:` line")


def _uncommented(path) -> list[str]:
    return [
        ln for ln in (REPO_ROOT / path).read_text(encoding="utf-8").splitlines()
        if not ln.lstrip().startswith("#")
    ]


def _site_lane_lines() -> list[str]:
    """ci.yml's uncommented lines, restricted to the site-lane jobs.

    Sliced by the top-level `  jobname:` indentation, so a PACKAGE job's
    python pins can never satisfy — or fail — a SITE-lane assertion.
    """
    lines = _uncommented(".github/workflows/ci.yml")
    kept: list[str] = []
    keeping = False
    for ln in lines:
        m = re.match(r"^  ([a-z][a-z0-9_-]*):\s*$", ln)
        if m:
            keeping = m.group(1) in SITE_LANE_JOBS
        if keeping:
            kept.append(ln)
    assert kept, "no site-lane jobs found — did a job in SITE_LANE_JOBS get renamed?"
    return kept


def _render_runtime() -> str:
    for ln in _uncommented("render.yaml"):
        m = re.match(r"\s*runtime:\s*(\S+)", ln)
        if m:
            return m.group(1)
    raise AssertionError("render.yaml declares no `runtime:`")


def test_dockerfile_tag_is_minor_only():
    """The patch pin IS the security bug: `3.11.8-slim` never receives a
    3.11.x fix release. The minor tag tracks them through Docker Hub."""
    tag = _fleet_minor()
    assert re.fullmatch(r"\d+\.\d+-slim", tag), (
        f"Dockerfile FROM tag is {tag!r} — must be a MINOR tag "
        "(python:X.Y-slim), never a patch pin"
    )


def test_render_yaml_agrees_with_the_image():
    """BRANCHES on the service runtime (1.6.28 — filed independently by
    three forks in the batch-2/3 round; the template is the reference
    implementation for BOTH branches, not just its own service type).

    `runtime: python` — the native runtime reads PYTHON_VERSION and
    requires a full X.Y.Z (its encoding, not ours): the value is
    REQUIRED and its MINOR must be the fleet Python. The patch needs a
    human bump now and then; the minor drifting is the class this file
    exists for.

    `runtime: docker` — this service's branch: NOTHING reads
    PYTHON_VERSION; the image is the interpreter. The key must be
    ABSENT: a value there reads like the platform's setting and can
    never be true — the item's own defect class (a declaration nothing
    holds to reality) arriving through the fix. If the runtime ever
    changes, this test flips branches by itself.

    Anything else fails loudly: extend the branch deliberately, never
    by accident."""
    minor = _fleet_minor().removesuffix("-slim")
    runtime = _render_runtime()
    lines = _uncommented("render.yaml")
    value = None
    for i, ln in enumerate(lines):
        if re.match(r"\s*- key: PYTHON_VERSION$", ln):
            m = re.search(r'value:\s*"([^"]+)"', lines[i + 1])
            value = m and m.group(1)
            break
    if runtime == "docker":
        assert value is None, (
            f"render.yaml declares PYTHON_VERSION {value!r} on a docker "
            "runtime — nothing reads it there; a string that looks like "
            "the platform's setting and can never be true is the drift "
            "class this file exists to kill. Delete the key."
        )
        return
    assert runtime == "python", (
        f"render.yaml runtime is {runtime!r} — this test knows `python` "
        "and `docker`; extend the branch deliberately"
    )
    assert value, "render.yaml declares no PYTHON_VERSION"
    assert re.fullmatch(r"\d+\.\d+\.\d+", value), (
        f"PYTHON_VERSION {value!r} — Render requires full X.Y.Z"
    )
    assert value.startswith(minor + "."), (
        f"render.yaml PYTHON_VERSION {value} vs image python:{minor}-slim — "
        "the native-runtime lane and the image lane disagree"
    )


def test_ci_matrix_main_and_singleton_jobs_agree_with_the_image():
    """SITE-lane pins only (see the module docstring): lint, docs-tests,
    the smoke matrix's main, and pip-audit are held to the image's minor.
    The package jobs' pins are the wheel's `python_requires` claim, not a
    site declaration, and are sliced out before the greps run."""
    minor = _fleet_minor().removesuffix("-slim")
    ci = _site_lane_lines()

    mains = [m.group(1) for ln in ci
             if (m := re.match(r'\s*python:\s*\["([\d.]+)"\]', ln))]
    assert mains == [minor], (
        f"ci.yml site-lane matrix main {mains} vs image python:{minor}-slim"
    )

    # lint, docs-tests and pip-audit run literal python-version pins; the
    # smoke job's is `${{ matrix.python }}` and is deliberately not a literal.
    literals = [m.group(1) for ln in ci
                if (m := re.match(r'\s*python-version:\s*"([\d.]+)"', ln))]
    assert literals and set(literals) == {minor}, (
        f"ci.yml site-lane singleton jobs pin {literals}, "
        f"image is python:{minor}-slim"
    )

    cd = _uncommented(".github/workflows/cd.yml")
    cd_literals = [m.group(1) for ln in cd
                   if (m := re.match(r'\s*python-version:\s*"([\d.]+)"', ln))]
    assert cd_literals and set(cd_literals) == {minor}, (
        f"cd.yml verify job pins {cd_literals}, image is python:{minor}-slim"
    )


def test_matrix_legs_are_the_adjacent_minors():
    """The compat window stays three wide: the include legs are X.Y-1 and
    X.Y-2 (or X.Y+1 once it exists). In this fork's matrix the include
    rows spell `python:` as a plain mapping key (the dash-axis rows pin a
    window-leg python too, which keeps them inside the same window), so
    the grep accepts both the `- python:` and bare `python:` spellings.
    These are SITE-lane legs; the PACKAGE matrix's 3.9–3.13 range lives
    outside this window's scope entirely."""
    major, y = (int(p) for p in _fleet_minor().removesuffix("-slim").split("."))
    allowed = {f"{major}.{y}", f"{major}.{y - 1}", f"{major}.{y - 2}",
               f"{major}.{y + 1}"}
    ci = _site_lane_lines()
    legs = [m.group(1) for ln in ci
            if (m := re.match(r'\s*(?:- )?python:\s*"([\d.]+)"', ln))]
    assert legs, "the matrix has no include legs — the window collapsed to one"
    outside = [leg for leg in legs if leg not in allowed]
    assert not outside, (
        f"matrix legs {outside} fall outside the three-wide window around "
        f"{major}.{y}"
    )
