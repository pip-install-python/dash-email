"""
dash_email - Dash components wrapping React Email for building email templates

A Plotly Dash component library that wraps React Email components,
enabling Python developers to build and preview email templates
directly within Dash applications.

Basic usage:
    import dash_email as de

    email = de.Email([
        de.EmailBody([
            de.EmailContainer([
                de.EmailHeading("Welcome!", as_="h1"),
                de.EmailText("Thanks for signing up."),
                de.EmailButton("Get Started", href="https://example.com")
            ])
        ])
    ])
"""
import json
import os

from ._imports_ import *  # noqa: F401,F403
from ._imports_ import __all__

_current_path = os.path.dirname(os.path.abspath(__file__))

_js_dist = [
    {
        'relative_package_path': 'dash_email.min.js',
        'namespace': 'dash_email'
    }
]

_css_dist = []

# Load package info for version
try:
    with open(os.path.join(_current_path, 'package.json')) as f:
        package = json.load(f)
        __version__ = package.get('version', '0.0.1')
except FileNotFoundError:
    __version__ = '0.0.1'