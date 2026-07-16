# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentSingleType = typing.Union[str, int, float, Component, None]
ComponentType = typing.Union[
    ComponentSingleType,
    typing.Sequence[ComponentSingleType],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class EmailFont(Component):
    """An EmailFont component.
EmailFont loads a custom font for use in the email.
In preview mode, this adds a style tag with @font-face.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- fallbackFontFamily (string | list of strings; default 'Helvetica'):
    Fallback font family if the web font fails to load.

- fontFamily (string; required):
    The font family name.

- fontStyle (string; default 'normal'):
    Font style (normal, italic).

- fontWeight (number | string; default 400):
    Font weight (400, 700, bold, etc.).

- webFont (dict; optional):
    Web font configuration object with url and format properties.

    `webFont` is a dict with keys:

    - url (string; required)

    - format (string; required)"""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_email'
    _type = 'EmailFont'
    WebFont = TypedDict(
        "WebFont",
            {
            "url": str,
            "format": str
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        fontFamily: typing.Optional[str] = None,
        fallbackFontFamily: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        webFont: typing.Optional["WebFont"] = None,
        fontStyle: typing.Optional[str] = None,
        fontWeight: typing.Optional[typing.Union[NumberType, str]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'fallbackFontFamily', 'fontFamily', 'fontStyle', 'fontWeight', 'webFont']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'fallbackFontFamily', 'fontFamily', 'fontStyle', 'fontWeight', 'webFont']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['fontFamily']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(EmailFont, self).__init__(**args)

setattr(EmailFont, "__init__", _explicitize_args(EmailFont.__init__))
