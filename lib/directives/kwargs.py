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


def resolve_kwargs(spec: str, default_package: str = "dash_email") -> tuple[str, list[dict]]:
    """Resolve a `.. kwargs::` spec (`EmailButton`, `dmc.Button`, ...) to
    ``(component_name, prop_rows)``.

    RAISES on failure (bad package, bad component name, no docstring) — on
    purpose, so a broken spec cannot render as silence. Both the browser
    lane (Kwargs.hook, below) and the machine lane
    (pages/markdown.py's ``.. kwargs::`` expansion into `/<page>/llms.txt`)
    call this one function, so import and docstring resolution happens in
    exactly ONE place for both consumers — sync item 18's "fourth
    mechanism": a directive whose output lives only in the React tree while
    the machine lane reads the raw, un-expanded markdown source.
    """
    if "." in spec:
        package_abbr, component_name = spec.rsplit(".", 1)
        package = PACKAGE_MAP.get(package_abbr, package_abbr)
    else:
        package, component_name = default_package, spec
    imported = importlib.import_module(package)
    component = getattr(imported, component_name)
    docstring = inspect.getdoc(component).split("Keyword arguments:")[-1]
    return component_name, convert_docstring_to_dict(docstring)


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
            default_package = attrs.pop("library", "dash_email")

            try:
                component_name, kwargs = resolve_kwargs(spec, default_package)
                attrs["kwargs"] = kwargs
                attrs["title"] = component_name
            except Exception:
                attrs["kwargs"] = []
