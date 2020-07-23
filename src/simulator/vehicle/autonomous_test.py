import typing
import unittest
from unittest.mock import Mock

from simulator.position import Position
from simulator.vehicle.autonomous import AutonomousCar, isAutonomous
from simulator.vehicle.obstacle import Obstacle
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
        self.assertEqual(limit, 5)
        # Vehicle in front is far away.
        road.getNextVehicle.return_value = (10, Mock())
        limit = car._getMaxSpeed(position=(0, 0))
        self.assertEqual(limit, 5)
        # Vehicle in front is blocking the road.
        road.getNextVehicle.return_value = (2, Mock())
        limit = car._getMaxSpeed(position=(0, 0))
        self.assertEqual(limit, 1)
        # Vehicle in front is autonomous.
        other = AutonomousCar(position=(1, 0), velocity=3, road=road)
        road.getNextVehicle.return_value = (1, other)
        limit = car._getMaxSpeed(position=(0, 0))
        self.assertEqual(limit, 3)
        other.velocity = 5
        road.getNextVehicle.return_value = (1, other)
        limit = car._getMaxSpeed(position=(0, 0))
        self.assertEqual(limit, 5)

    def test_tryAvoidObstacle(self):
        # No obstacles on the road.
        road = Mock(lane_width=1)
        road.getNextVehicle.return_value = -1, None
        car = AutonomousCar(position=(42, 1), velocity=5, road=road)
        self.assertFalse(car._tryAvoidObstacle())
        # Not an obstacle on the road in front.
        road = Mock(lane_width=1)
        road.getNextVehicle.return_value = 44, Mock()
        car = AutonomousCar(position=(42, 1), velocity=5, road=road)
        self.assertFalse(car._tryAvoidObstacle())
        # Obstacle is far away.
        road = Mock(lane_width=1)
        road.getNextVehicle.return_value = 120, Obstacle(position=(120, 2), length=1, width=1)
        car = AutonomousCar(position=(42, 1), velocity=5, road=road)
        self.assertFalse(car._tryAvoidObstacle())

        def mock_getMaxSpeed(prev: int, next: int, other: int) -> typing.Callable[[Position], int]:
            def f(position: Position) -> int:
                if position == (0, 0):
                    return prev
                if position == (0, 2):
                    return next
                return other

            return f

        road = Mock(lane_width=1)
        road.getNextVehicle.return_value = 5, Obstacle(position=(5, 1), length=1, width=1)
        # Unable to change lanes.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._canAvoidObstacle = Mock(return_value=False)
        car._avoidObstacle = Mock()
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(5, 4, 3))
        self.assertFalse(car._tryAvoidObstacle())
        car._avoidObstacle.assert_not_called()
        self.assertEqual(car.position, (0, 1))
        # Previous lane is the fastest.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._canAvoidObstacle = Mock(return_value=True)
        car._avoidObstacle = Mock()
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(5, 4, 3))
        self.assertTrue(car._tryAvoidObstacle())
        car._avoidObstacle.assert_called_once()
        self.assertEqual(car.position, (0, 0))
        # Next lane is the fastest.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._canAvoidObstacle = Mock(return_value=True)
        car._avoidObstacle = Mock()
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(4, 5, 3))
        self.assertTrue(car._tryAvoidObstacle())
        car._avoidObstacle.assert_called_once()
        self.assertEqual(car.position, (0, 2))
        # Current lane is the fastest.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._canAvoidObstacle = Mock(return_value=True)
        car._avoidObstacle = Mock()
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(4, 3, 5))
        self.assertFalse(car._tryAvoidObstacle())
        car._avoidObstacle.assert_not_called()
        self.assertEqual(car.position, (0, 1))
        # Best lane is the same speed as current.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._canAvoidObstacle = Mock(return_value=True)
        car._avoidObstacle = Mock()
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(5, 4, 5))
        self.assertFalse(car._tryAvoidObstacle())
        car._avoidObstacle.assert_not_called()
        self.assertEqual(car.position, (0, 1))

    def test_tryChangeLanes(self):
        def mock_getMaxSpeed(prev: int, next: int, other: int) -> typing.Callable[[Position], int]:
            def f(position: Position) -> int:
                if position == (0, 0):
                    return prev
                if position == (0, 2):
                    return next
                return other

            return f

        road = Mock(lane_width=1)
        # Unable to change lanes.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._canChangeLane = Mock(return_value=False)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(5, 4, 3))
        self.assertFalse(car._tryChangeLanes())
        self.assertEqual(car.position, (0, 1))
        # Previous lane is the fastest.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._canChangeLane = Mock(return_value=True)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(5, 4, 3))
        self.assertTrue(car._tryChangeLanes())
        self.assertEqual(car.position, (0, 0))
        # Next lane is the fastest.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._canChangeLane = Mock(return_value=True)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(4, 5, 3))
        self.assertTrue(car._tryChangeLanes())
        self.assertEqual(car.position, (0, 2))
        # Current lane is the fastest.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._canChangeLane = Mock(return_value=True)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(4, 3, 5))
        self.assertFalse(car._tryChangeLanes())
        self.assertEqual(car.position, (0, 1))
        # Best lane is the same speed as current.
        car = AutonomousCar(position=(0, 1), velocity=5, road=road)
        car._canChangeLane = Mock(return_value=True)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(5, 4, 5))
        self.assertFalse(car._tryChangeLanes())
        self.assertEqual(car.position, (0, 1))

    def test_isAutonomous(self):
        car = self.getVehicle(position=(0, 0))
        self.assertTrue(isAutonomous(car))
        vehicle = Vehicle(position=(0, 0), velocity=0)
        self.assertFalse(isAutonomous(vehicle))


if __name__ == '__main__':
    unittest.main()
