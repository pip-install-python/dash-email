"""The network bulletin — wired, or off, and never a comment.

NETWORK FILE: adapted from dash-documentation-boilerplate 1.2.4, where this
existed because the wiring had sat COMMENTED OUT in run.py for weeks against a
hub endpoint that was already serving. Nothing failed. `configure_bulletin` is
opt-in, so an unwired app makes no request at all and the viewer header renders
perfectly well on the package's built-in tips and an "No announcements." empty
state. The only symptom was an announcement that never appeared — which nobody
goes looking for.

The load-bearing test is the last one: commented-out wiring cannot define the
name it asserts on, so it fails the moment somebody comments it out again.
"""

from __future__ import annotations

import pytest

from conftest import REPO_ROOT


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    """conftest pins NETWORK_BULLETIN_URL to "" for the whole session; these
    tests set it themselves and must not leak it into the others."""
    monkeypatch.delenv("NETWORK_BULLETIN_URL", raising=False)
    monkeypatch.delenv("NETWORK_BULLETIN_TTL_S", raising=False)


def test_no_url_means_the_feature_is_simply_off():
    from lib import bulletin

    assert bulletin.url() is None
    assert bulletin.configure() is False


def test_configure_reports_that_it_wired(monkeypatch):
    from lib import bulletin

    monkeypatch.setenv("NETWORK_BULLETIN_URL", bulletin.HUB_BULLETIN_URL)

    seen = {}

    def fake_configure_bulletin(**kwargs):
        seen.update(kwargs)

    import dash_improve_my_llms

    monkeypatch.setattr(dash_improve_my_llms, "configure_bulletin",
                        fake_configure_bulletin)

    assert bulletin.configure() is True
    assert seen["url"] == bulletin.HUB_BULLETIN_URL
    assert seen["app_id"] == "email"


def test_the_app_id_is_the_directory_key_not_a_second_opinion(app_module):
    """One id on every hub surface. A satellite still announcing itself as
    "boilerplate" would receive the template's announcements.

    `app_module` is load-bearing, not incidental: since the gate-wave pass the
    reporter is BYTE-IDENTICAL to the template's, so its own fallback says
    "boilerplate" — the "email" identity comes from run.py's fork point
    (`os.environ.setdefault("SATELLITE_APP_KEY", "email")`), which only exists
    once run.py has imported.
    """
    from lib import bulletin
    from lib.satellite_reporter import app_key

    assert bulletin.app_id() == app_key() == "email"


def test_every_hub_surface_names_this_app_the_same_way(app_module):
    """Ads, traffic, the bulletin and the hub client all say "email".

    Four modules present an identity to the hub and each has its own
    fallback, so they can drift apart without anything failing — the symptom
    is a column on /admin/ad-analytics that does not line up with /traffic,
    which nobody reconciles. The byte-copied reporter's own fallback says
    "boilerplate" (deliberately — shasum vs the template is the acceptance
    check); run.py's fork point is what closes that gap, and this test is
    what fails if a future sync drops that one line (the pannellum
    contamination, 2026-08-21).
    """
    import os

    from lib import ad_client, bulletin, hub_client, satellite_reporter

    assert os.environ.get("SATELLITE_APP_KEY") == "email", (
        "run.py's fork point did not claim this app's identity"
    )
    assert ad_client.APP_ID == "email"
    assert satellite_reporter.app_key() == "email"
    assert hub_client.app_id() == "email"
    assert bulletin.app_id() == "email"


def test_a_bad_ttl_falls_back_rather_than_crashing_the_boot(monkeypatch):
    from lib import bulletin

    monkeypatch.setenv("NETWORK_BULLETIN_TTL_S", "not-a-number")
    assert bulletin._ttl() == bulletin.DEFAULT_TTL_S
    monkeypatch.setenv("NETWORK_BULLETIN_TTL_S", "5")
    assert bulletin._ttl() == 60.0, "a too-short TTL would hammer the hub"


def test_run_py_wires_it_rather_than_leaving_it_commented_out():
    """The regression this file exists for.

    Commented-out wiring cannot define the name it asserts on, so requiring a
    real call here is what makes commenting it out fail loudly.
    """
    source = (REPO_ROOT / "run.py").read_text()
    live = "\n".join(
        line for line in source.splitlines() if not line.strip().startswith("#")
    )
    assert "bulletin.configure()" in live, (
        "run.py no longer calls bulletin.configure() outside a comment"
    )
