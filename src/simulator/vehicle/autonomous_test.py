import unittest
from unittest.mock import Mock

from simulator.position import Position
from simulator.vehicle.autonomous import AutonomousCar
from simulator.vehicle.vehicle import Vehicle
from simulator.vehicle.vehicle_test import implementsVehicle


@implementsVehicle
class AutonomousCarTestCase(unittest.TestCase):
    def getVehicle(self, position: Position) -> Vehicle:
        road = Mock()
        road.isProperPosition.return_value = False
        road.getNextVehicle.return_value = (10000, None)
        road.getPreviousVehicle.return_value = (-1, None)
        road.controller = Mock()
        road.controller.getMaxSpeed.return_value = 5
        return AutonomousCar(position=position, velocity=1, road=road)


if __name__ == '__main__':
    unittest.main()
