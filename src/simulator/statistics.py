import typing

from simulator.vehicle.vehicle import Vehicle

Statistics = typing.Dict[str, typing.Any]

Filter = typing.Callable[[Vehicle], bool]


def combine(*predicates: Filter) -> Filter:
    return lambda vehicle: all((predicate(vehicle) for predicate in predicates))


def filterLane(lane: int) -> Filter:
    return lambda vehicle: vehicle.position[1] == lane
