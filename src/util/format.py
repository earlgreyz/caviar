import typing

T = typing.TypeVar('T')


class OptionalFormat(typing.Generic[T]):  # The wrapper is not type-specific
    def __init__(self, value: typing.Optional[T]):
        self.value = value

    def __format__(self, *args, **kwargs) -> str:
        if self.value is None:
            return '~'
        else:
            return self.value.__format__(*args, **kwargs)
