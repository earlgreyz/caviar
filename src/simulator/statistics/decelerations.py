from more_itertools import ilen

from simulator.vehicle.car import Car
from simulator.vehicle.vehicle import Vehicle
from simulator.road.road import Road
from simulator.statistics.filters import Filter, combine


def getDecelerationsFiltered(road: Road, predicate: Filter) -> int:
    def isDeceleration(vehicle: Vehicle) -> bool:
        if not isinstance(vehicle, Car):
            return False
        _, last_velocity = vehicle.path[-1]
        return last_velocity - vehicle.velocity > 1

    return ilen(filter(combine(predicate, isDeceleration), road.getAllVehicles()))


def getDecelerations(road: Road) -> int:
    return getDecelerationsFiltered(road, lambda _: True)
