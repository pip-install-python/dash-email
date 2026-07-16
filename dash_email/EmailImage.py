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


class EmailImage(Component):
    """An EmailImage component.
EmailImage renders an image in the email.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- alt (string; default ''):
    Alternative text for the image.

- height (number | string; optional):
    The height of the image (number or string).

- src (string; required):
    The image source URL. Should be an absolute URL for production.

- width (number | string; optional):
    The width of the image (number or string like \"100%\")."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_email'
    _type = 'EmailImage'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        src: typing.Optional[str] = None,
        alt: typing.Optional[str] = None,
        width: typing.Optional[typing.Union[NumberType, str]] = None,
        height: typing.Optional[typing.Union[NumberType, str]] = None,
        style: typing.Optional[typing.Any] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'alt', 'height', 'src', 'style', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'alt', 'height', 'src', 'style', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['src']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(EmailImage, self).__init__(**args)

setattr(EmailImage, "__init__", _explicitize_args(EmailImage.__init__))
