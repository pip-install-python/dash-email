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


class Email(Component):
    """An Email component.
Email is the root wrapper component for email templates.
Renders as an HTML document structure suitable for email preview.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component (EmailHead, EmailPreview,
    EmailBody, etc.).

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- dir (a value equal to: 'ltr', 'rtl'; default 'ltr'):
    Text direction of the email content.

- lang (string; default 'en'):
    Language of the email content."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_email'
    _type = 'Email'


    def __init__(
        self,
        children: typing.Optional[ComponentType] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        lang: typing.Optional[str] = None,
        dir: typing.Optional[Literal["ltr", "rtl"]] = None,
        style: typing.Optional[typing.Any] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'dir', 'lang', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'dir', 'lang', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Email, self).__init__(children=children, **args)

setattr(Email, "__init__", _explicitize_args(Email.__init__))
