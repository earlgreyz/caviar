import typing

from util.sizedlist import SizedList

T = typing.TypeVar('T')


class CumulativeList(SizedList[T]):
    def __init__(self, size: int, *items: T):
        super().__init__(size + 1, *items)

    def append(self, item: T) -> None:
        if len(self) == 0:
            super().append(item)
        else:
            super().append(item + self[-1])

    def value(self) -> T:
        if len(self) < self.size:
            return self[-1]
        else:
            return self[-1] - self[0]
