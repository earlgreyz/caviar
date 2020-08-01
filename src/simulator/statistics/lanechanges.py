from simulator.road.road import Road
from simulator.statistics.filters import Filter


def getLaneChangesFiltered(road: Road, predicate: Filter) -> int:
    lane_changes = 0
    for vehicle in filter(predicate, road.getAllVehicles()):
        _, last_lane = vehicle.last_position
        _, lane = vehicle.position
        if last_lane != lane:
            lane_changes += 1
    return lane_changes


def getLaneChanges(road: Road) -> int:
    return getLaneChangesFiltered(road, lambda _: True)
