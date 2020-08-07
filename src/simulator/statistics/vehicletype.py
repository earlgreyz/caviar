import enum

from simulator.statistics.filters import Filter
from simulator.vehicle.autonomous import isAutonomous
from simulator.vehicle.car import isCar
from simulator.vehicle.conventional import isConventional


class VehicleType(enum.Enum):
    AUTONOMOUS = enum.auto()
    CONVENTIONAL = enum.auto()
    ANY = enum.auto()


def getVehicleTypeFilter(vehicle_type: VehicleType) -> Filter:
    if vehicle_type is VehicleType.CONVENTIONAL:
        return isConventional
    elif vehicle_type is VehicleType.AUTONOMOUS:
        return isAutonomous
    elif vehicle_type is VehicleType.ANY:
        return isCar
    assert False, 'unreachable'


def getVehicleTypeName(vehicle_type: VehicleType) -> str:
    if vehicle_type is VehicleType.CONVENTIONAL:
        return 'conventional'
    elif vehicle_type is VehicleType.AUTONOMOUS:
        return 'autonomous'
    elif vehicle_type is VehicleType.ANY:
        return 'all'
    assert False, 'unreachable'
