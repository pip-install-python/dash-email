# Utils module
#
# Submodules are imported lazily (PEP 562) so that importing one helper does not
# pull in optional third-party clients. gemini_handler needs a Google API key,
# and importing it eagerly here made every consumer of utils.* fail at import
# time when the key was absent.

__all__ = ['generate_email_content', 'send_email']

_LAZY_ATTRS = {
    'generate_email_content': '.gemini_handler',
    'send_email': '.email_sender',
}


def __getattr__(name):
    if name in _LAZY_ATTRS:
        from importlib import import_module

        module = import_module(_LAZY_ATTRS[name], __name__)
        value = getattr(module, name)
        globals()[name] = value  # cache so the import runs once per attribute
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(list(globals()) + __all__)
