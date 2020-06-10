import typing

from simulator.vehicle.vehicle import Vehicle

Statistics = typing.Dict[str, typing.Any]

Filter = typing.Callable[[Vehicle], bool]


def combine(*predicates: Filter) -> Filter:
    return lambda vehicle: all((predicate(vehicle) for predicate in predicates))


def filterLane(lane: int) -> Filter:
    return lambda vehicle: vehicle.position[1] == lane


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
