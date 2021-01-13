__all__ = ['OpenCloseMixin']

from abc import ABC
from typing import Callable, Type

from .decorators import (
    only_while_open, only_while_closed, always, check_status
)


class OpenCloseMixin(ABC):
    '''Mixin for classes with open-close dynamics.'''

    not_open_exception = ValueError(
        'The instance is not open and the method "{method_name}" cannot run '
        'under such condition.'
    )

    not_closed_exception = ValueError(
        'The instance is not closed and the method "{method_name}" cannot run '
        'under such condition.'
    )

    def __init_subclass__(
        cls: Type['OpenCloseMixin'], **kwargs
    ) -> Type['OpenCloseMixin']:
        for attr_name in cls.__dict__:
            if not isinstance(attr := getattr(cls, attr_name), Callable):
                continue

            if not hasattr(attr, '_when'):
                if attr_name == '__init__':
                    setattr(cls, attr_name, always(attr))
                elif attr_name == 'open':
                    setattr(cls, attr_name, only_while_closed(attr))
                else:
                    setattr(cls, attr_name, only_while_open(attr))

            setattr(cls, attr_name, check_status(attr))

        return cls

    @check_status
    @only_while_closed
    def open(self: 'OpenCloseMixin') -> None:
        self._open = True

    @check_status
    @only_while_open
    def close(self: 'OpenCloseMixin') -> None:
        self._open = False
