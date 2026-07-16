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


class EmailButton(Component):
    """An EmailButton component.
EmailButton renders a styled link that looks like a button.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The button label/content.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- href (string; required):
    The URL to navigate to when clicked.

- target (string; default '_blank'):
    Where to open the link (_blank, _self, etc.)."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_email'
    _type = 'EmailButton'


    def __init__(
        self,
        children: typing.Optional[ComponentType] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        href: typing.Optional[str] = None,
        target: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'href', 'style', 'target']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'href', 'style', 'target']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['href']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(EmailButton, self).__init__(children=children, **args)

setattr(EmailButton, "__init__", _explicitize_args(EmailButton.__init__))
