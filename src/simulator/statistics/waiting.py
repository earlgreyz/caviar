from more_itertools import ilen

from simulator.road.road import Road
from simulator.statistics.filters import Filter, combine
from simulator.vehicle.vehicle import Vehicle


def getWaitingFiltered(road: Road, predicate: Filter) -> int:
    def isWaiting(vehicle: Vehicle) -> bool:
        return vehicle.position == vehicle.last_position

    return ilen(filter(combine(predicate, isWaiting), road.getAllVehicles()))


def getWaiting(road: Road) -> int:
    return getWaitingFiltered(road, lambda _: True)
