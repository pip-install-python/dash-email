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


class EmailPreview(Component):
    """An EmailPreview component.
EmailPreview renders preview text that appears in the inbox
before the email is opened. Hidden in the actual email body.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The preview text to display in email client inboxes.

- id (string; optional):
    The ID used to identify this component in Dash callbacks."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_email'
    _type = 'EmailPreview'


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

        super(EmailPreview, self).__init__(children=children, **args)

setattr(EmailPreview, "__init__", _explicitize_args(EmailPreview.__init__))
