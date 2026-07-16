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


class EmailHead(Component):
    """An EmailHead component.
EmailHead contains metadata for the email such as fonts.
In preview mode, this renders as a hidden container.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component (EmailFont, style elements, etc.).

- id (string; optional):
    The ID used to identify this component in Dash callbacks."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_email'
    _type = 'EmailHead'


    def __init__(
        self,
        children: typing.Optional[ComponentType] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(EmailHead, self).__init__(children=children, **args)

setattr(EmailHead, "__init__", _explicitize_args(EmailHead.__init__))
