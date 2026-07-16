import importlib
import inspect

from markdown2dash.src.directives.kwargs import Kwargs as KwargsBase
from markdown2dash.src.utils import convert_docstring_to_dict

# Abbreviations usable in `.. kwargs::de.EmailButton` style directives.
PACKAGE_MAP = {
    "de": "dash_email",
    "dmc": "dash_mantine_components",
    "html": "dash.html",
    "dcc": "dash.dcc",
}


class Kwargs(KwargsBase):
    """Props table for Dash components.

    Dash-generated component docstrings use the `Keyword arguments:` format
    with `- name (type): description` blocks, which the upstream
    convert_docstring_to_dict already understands. This subclass only adds
    package resolution (default: dash_email) so docs can write
    `.. kwargs::EmailButton` or `.. kwargs::dmc.Button`.
    """

    def hook(self, md, state):
        for tok in state.tokens:
            if tok["type"] != self.block_name:
                continue
            attrs = tok["attrs"]
            spec = attrs["title"]

            if "." in spec:
                package_abbr, component_name = spec.rsplit(".", 1)
                package = PACKAGE_MAP.get(package_abbr, package_abbr)
            else:
                package = attrs.pop("library", "dash_email")
                component_name = spec

            try:
                imported = importlib.import_module(package)
                component = getattr(imported, component_name)
                docstring = inspect.getdoc(component).split("Keyword arguments:")[-1]
                attrs["kwargs"] = convert_docstring_to_dict(docstring)
                attrs["title"] = component_name
            except Exception:
                attrs["kwargs"] = []
