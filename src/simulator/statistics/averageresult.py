import typing


class AverageResult:
    value: int
    count: int

    def __init__(self, value, count):
        self.value = value
        self.count = count

    def __eq__(self, other: 'AverageResult') -> bool:
        return self.value == other.value and self.count == other.count

    def __add__(self, other: 'AverageResult') -> 'AverageResult':
        return AverageResult(value=self.value + other.value, count=self.count + other.count)

    def __sub__(self, other: 'AverageResult') -> 'AverageResult':
        return AverageResult(value=self.value - other.value, count=self.count - other.count)

    def __float__(self) -> float:
        return float(self.value) / self.count

    def __str__(self) -> str:
        return '{}/{}'.format(self.value, self.count)

    def toMaybeFloat(self) -> typing.Optional[float]:
        if self.count == 0:
            return None
        return float(self)
