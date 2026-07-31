"""Bootstrap that runs the smoke suite under a foreign interpreter.

Used by ``compat_matrix.py --local``. The target interpreter supplies **Dash**
(the thing under test); this project's own virtualenv supplies the docs-site
libraries that Dash version does not have installed.

Import order is the whole trick:

1. ``import dash`` FIRST, so it resolves from the target interpreter's own
   ``site-packages`` and lands in ``sys.modules``. Being cached there makes it
   immune to anything that follows, and its submodules resolve through the
   already-loaded package's ``__path__``.
2. Then PREPEND the donor ``site-packages``, so every *other* library comes
   from this project's virtualenv.

Step 2 used to append instead, which meant the target's own copy of a
non-Dash package silently won. That made the measurement depend on which
sibling venv the version scan happened to pick first: the venvs for Dash 4.2
and 4.3 carry ``dash-improve-my-llms`` 2.0.0, so those rows were quietly
measuring the OLD package while 4.1 and 4.4.1 measured 2.3.3 — five phantom
failures attributable to nothing in Dash. Only Dash may come from the target;
that is the entire claim this harness makes.

Env:
    DE_EXTRA_SITE   donor site-packages directory
    DE_SMOKE_ARGS   arguments to forward to smoke_test.py, newline-separated
"""
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 1. Pin Dash from the TARGET interpreter before anything else can pull one in.
import dash  # noqa: E402,F401

_resolved = dash.__version__
_origin = Path(dash.__file__).resolve()

# 2. Lend the target this project's libraries, ahead of its own — but ONLY
#    when the interpreters share a minor version. The donor holds compiled
#    extensions (pydantic_core, pandas, ...) built for one ABI; putting a
#    cpython-312 build ahead of a 3.13 interpreter's own copies turns the
#    whole run into "ModuleNotFoundError: pydantic_core._pydantic_core".
#    Appending instead is the safe degradation: the target keeps its own
#    libraries, so the row still measures Dash, just not this project's
#    dependency set. compat_matrix.py prefers a matching venv precisely so
#    this branch stays unused.
extra = os.environ.get("DE_EXTRA_SITE")
_donor_ok = True
if extra:
    donor_py = Path(extra).parent.name           # .../lib/python3.x/site-packages
    own_py = f"python{sys.version_info.major}.{sys.version_info.minor}"
    _donor_ok = donor_py == own_py
    while extra in sys.path:
        sys.path.remove(extra)
    if _donor_ok:
        sys.path.insert(0, extra)
    else:
        sys.path.append(extra)
        print(f"[runner] WARNING donor is {donor_py} but this is {own_py} — "
              "appended instead of prepended; the target's own libraries win")

# Report what actually got used, so a silently-wrong measurement is visible.
# dash-improve-my-llms is named explicitly because it owns robots.txt, the
# canonical/prerender layer and the network directory — the exact surface the
# smoke suite's [seo] group asserts on.
print(f"[runner] dash {_resolved} from {_origin.parent.parent.parent.parent}")
print(f"[runner] donor site-packages: {extra or '(none)'}")
try:
    import dash_improve_my_llms as _dimll

    print(f"[runner] dash-improve-my-llms {getattr(_dimll, '__version__', '?')} "
          f"from {Path(_dimll.__file__).resolve().parent.parent}")
except Exception as _exc:  # noqa: BLE001
    print(f"[runner] dash-improve-my-llms unavailable: {_exc}")

sys.argv = ["smoke_test.py"] + [
    a for a in (os.environ.get("DE_SMOKE_ARGS") or "").split("\n") if a
]
runpy.run_path(str(ROOT / "scripts" / "smoke_test.py"), run_name="__main__")
