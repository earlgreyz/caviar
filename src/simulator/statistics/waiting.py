from simulator.road.road import Road
from simulator.statistics.filters import Filter


def getWaitingFiltered(road: Road, predicate: Filter) -> int:
    waiting = 0
    for vehicle in filter(predicate, road.getAllVehicles()):
        if vehicle.position == vehicle.last_position:
            waiting += 1
    return waiting


def getWaiting(road: Road) -> int:
    return getWaitingFiltered(road, lambda _: True)
