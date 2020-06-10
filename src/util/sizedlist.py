import typing

T = typing.TypeVar('T')


class SizedList(typing.Generic[T]):
    size: int
    index: int
    items: typing.List[T]

    def __init__(self, size: int):
        self.size = size
        self.index = 0
        self.items = []

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> typing.Generator[T, None, None]:
        for i in range(self.index, len(self.items)):
            yield self.items[i]
        for i in range(0, self.index):
            yield self.items[i]

    def __getitem__(self, item: int) -> T:
        if item < -len(self) or item >= len(self):
            raise KeyError
        return self.items[(self.index + item) % len(self)]

    def insert(self, item: T) -> None:
        if len(self) < self.size:
            self.items.append(item)
        else:
            self.items[self.index] = item
            self.index = (self.index + 1) % self.size
