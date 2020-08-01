from simulator.vehicle.car import Car
from simulator.road.road import Road
from simulator.statistics.filters import Filter


def getDecelerationsFiltered(road: Road, predicate: Filter) -> int:
    decelerations = 0
    for vehicle in filter(predicate, road.getAllVehicles()):
        if not isinstance(vehicle, Car):
            continue
        _, last_velocity = vehicle.path[-1]
        if last_velocity - vehicle.velocity > 1:
            decelerations += 1
    return decelerations


def getDecelerations(road: Road) -> int:
    return getDecelerationsFiltered(road, lambda _: True)
