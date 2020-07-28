from simulator.road.road import Road
from simulator.statistics.averageresult import AverageResult
from simulator.statistics.filters import Filter


def getAverageVelocityFiltered(road: Road, predicate: Filter) -> AverageResult:
    velocity, count = 0, 0
    for vehicle in filter(predicate, road.getAllVehicles()):
        velocity += vehicle.velocity
        count += 1
    return AverageResult(value=velocity, count=count)


def getAverageVelocity(road: Road) -> AverageResult:
    return getAverageVelocityFiltered(road, lambda _: True)
