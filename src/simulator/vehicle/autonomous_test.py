import typing
import unittest
from unittest.mock import Mock

from simulator.position import Position
from simulator.vehicle.autonomous import AutonomousCar, isAutonomous
from simulator.vehicle.vehicle import Vehicle
from simulator.vehicle.vehicle_test import implementsVehicle


@implementsVehicle
class AutonomousCarTestCase(unittest.TestCase):
    def getVehicle(self, position: Position) -> Vehicle:
        road = Mock(length=100, lane_width=1)
        road.isProperPosition.return_value = False
        road.getNextVehicle.return_value = (10000, None)
        road.getPreviousVehicle.return_value = (-1, None)
        road.controller = Mock()
        road.controller.getMaxSpeed.return_value = 5
        return AutonomousCar(position=position, velocity=1, road=road)

    def test_getMaxSpeed(self):
        road = Mock(length=100)
        road.controller = Mock()
        road.controller.getMaxSpeed.return_value = 5
        car = AutonomousCar(position=(0, 0), velocity=5, road=road)
        # No vehicles in front.
        road.getNextVehicle.return_value = (100, None)
        limit = car._getMaxSpeed(position=(0, 0))
        self.assertEqual(limit, 5, 'expected road limit')
        # Vehicle in front is far away.
        road.getNextVehicle.return_value = (10, Mock())
        limit = car._getMaxSpeed(position=(0, 0))
        self.assertEqual(limit, 5, 'expected road limit')
        # Vehicle in front is blocking the road.
        road.getNextVehicle.return_value = (2, Mock())
        limit = car._getMaxSpeed(position=(0, 0))
        self.assertEqual(limit, 1, 'expected min distance')
        # Vehicle in front is autonomous.
        other = AutonomousCar(position=(1, 0), velocity=3, road=road)
        road.getNextVehicle.return_value = (1, other)
        limit = car._getMaxSpeed(position=(0, 0))
        self.assertEqual(limit, 3, 'expected min distance with added velocity')
        other.velocity = 5
        road.getNextVehicle.return_value = (1, other)
        limit = car._getMaxSpeed(position=(0, 0))
        self.assertEqual(limit, 5, 'expected road limit')

    def test_beforeMove(self):
        def mock_getMaxSpeed(prev: int, next: int, other: int) -> typing.Callable[[Position], int]:
            def f(position: Position) -> int:
                if position == (0, 0):
                    return prev
                if position == (0, 2):
                    return next
                return other

            return f

        road = Mock(lane_width=1)
        # Previous lane is the fastest.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._changeLane = Mock(return_value=True)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(5, 4, 3))
        position = car.beforeMove()
        self.assertEqual(position, (0, 0))
        # Next lane is the fastest.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._changeLane = Mock(return_value=True)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(4, 5, 3))
        position = car.beforeMove()
        self.assertEqual(position, (0, 2))
        # Current lane is the fastest.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._changeLane = Mock(return_value=True)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(4, 3, 5))
        position = car.beforeMove()
        self.assertEqual(position, (0, 1))
        # Best lane is the same speed as current.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._changeLane = Mock(return_value=True)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(5, 4, 5))
        position = car.beforeMove()
        self.assertEqual(position, (0, 1))

    def test_isAutonomous(self):
        car = self.getVehicle(position=(0, 0))
        self.assertTrue(isAutonomous(car))
        vehicle = Vehicle(position=(0, 0), velocity=0)
        self.assertFalse(isAutonomous(vehicle))


if __name__ == '__main__':
    unittest.main()
