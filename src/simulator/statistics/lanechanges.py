from more_itertools import ilen

from simulator.road.road import Road
from simulator.statistics.filters import Filter, combine
from simulator.vehicle.vehicle import Vehicle


def getLaneChangesFiltered(road: Road, predicate: Filter) -> int:
    def isLaneChange(vehicle: Vehicle) -> bool:
        _, last_lane = vehicle.last_position
        _, lane = vehicle.position
        return last_lane != lane

    return ilen(filter(combine(predicate, isLaneChange), road.getAllActiveVehicles()))


def getLaneChanges(road: Road) -> int:
    return getLaneChangesFiltered(road, lambda _: True)
