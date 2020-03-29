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
        road = Mock()
        road.isProperPosition.return_value = False
        road.getNextVehicle.return_value = (10000, None)
        road.getPreviousVehicle.return_value = (-1, None)
        road.controller = Mock()
        road.controller.getMaxSpeed.return_value = 5
        return AutonomousCar(position=position, velocity=1, road=road)

    def test_getMaxSpeed(self):
        road = Mock()
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

    def test_canChangeLane(self):
        road = Mock()
        car = AutonomousCar(position=(0, 0), velocity=5, road=road)
        # All possible combinations, which doesn't allow for a change 2^3 - 1.
        ipps = [False, True, True, False, False, True, False]
        gvs = [None, Mock(), None, Mock(), None, Mock(), Mock()]
        gpvs = [None, None, Mock(), None, Mock(), Mock(), Mock()]
        for ipp, gv, gpv in zip(ipps, gvs, gpvs):
            road.isProperPosition.return_value = ipp
            road.getVehicle.return_value = gv
            road.getPendingVehicle.return_value = gpv
            self.assertFalse(car._canChangeLane(destination=(0, 1)), f'case=({ipp}, {gv}, {gpv})')
        # All conditions are met.
        road.isProperPosition.return_value = True
        road.getVehicle.return_value = None
        road.getPendingVehicle.return_value = None
        self.assertTrue(car._canChangeLane(destination=(0, 1)))

    def test_shouldChangeLane(self):
        road = Mock()
        position = (10, 0)
        destination = (10, 1)
        limit = 5
        car = AutonomousCar(position=position, velocity=limit + 1, road=road)

        def mock_getMaxSpeed(speed: int):
            return lambda position: limit if position == car.position else speed

        # Speed on the destination lane is lower or equal.
        for i in range(limit + 1):
            car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(i))
            self.assertFalse(car._shouldChangeLane(destination), f'destination speed={i}')
        # Velocity is higher than the distance to the next vehicle on the destination lane.
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(limit + 1))
        road.getNextVehicle.return_value = (10 + limit, Mock())
        self.assertFalse(car._shouldChangeLane(destination))
        # Same but autonomous vehicle with low velocity.
        other = AutonomousCar(position=(10 + limit, 0), velocity=1, road=road)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(limit + 1))
        road.getNextVehicle.return_value = (10 + limit, other)
        self.assertFalse(car._shouldChangeLane(destination))
        # The velocity of the autonomous vehicle in front is higher.
        other = AutonomousCar(position=(10 + limit, 0), velocity=5, road=road)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(limit + 1))
        road.getPreviousVehicle.return_value = (-1, None)
        road.getNextVehicle.return_value = (10 + limit, other)
        self.assertTrue(car._shouldChangeLane(destination))
        # A vehicle is approaching from behind.
        road.getNextVehicle.return_value = (100, None)
        road.controller.getMaxSpeed.return_value = 5
        road.getPreviousVehicle.return_value = (5, Mock())
        self.assertFalse(car._shouldChangeLane(destination))
        # Same but autonomous vehicle with high velocity.
        other = AutonomousCar(position=(10 - limit, 0), velocity=limit, road=road)
        road.getPreviousVehicle.return_value = (10 - limit, other)
        self.assertFalse(car._shouldChangeLane(destination))
        # The velocity of the autonomous vehicle behind is lower.
        other = AutonomousCar(position=(10 - limit, 0), velocity=limit - 1, road=road)
        road.getPreviousVehicle.return_value = (10 - limit, other)
        self.assertTrue(car._shouldChangeLane(destination))
        # Lane change is possible.
        road.getPreviousVehicle.return_value = (0, Mock())
        self.assertTrue(car._shouldChangeLane(destination))
        road.getPreviousVehicle.return_value = (-1, None)
        self.assertTrue(car._shouldChangeLane(destination))

    def test_beforeMove(self):
        def mock_getMaxSpeed(previous: int, next: int, other: int) \
                -> typing.Callable[[Position], int]:
            def f(position: Position) -> int:
                if position == (0, 0):
                    return previous
                if position == (0, 2):
                    return next
                return other

            return f

        # Previous lane is the fastest.
        car = AutonomousCar(position=(0, 1), velocity=5, road=Mock())
        car._canChangeLane = Mock(return_value=True)
        car._shouldChangeLane = Mock(return_value=True)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(5, 4, 3))
        position = car.beforeMove()
        self.assertEqual(position, (0, 0))
        # Next lane is the fastest.
        car = AutonomousCar(position=(0, 1), velocity=5, road=Mock())
        car._canChangeLane = Mock(return_value=True)
        car._shouldChangeLane = Mock(return_value=True)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(4, 5, 3))
        position = car.beforeMove()
        self.assertEqual(position, (0, 2))
        # Current lane is the fastest.
        car = AutonomousCar(position=(0, 1), velocity=5, road=Mock())
        car._canChangeLane = Mock(return_value=True)
        car._shouldChangeLane = Mock(return_value=True)
        car._getMaxSpeed = Mock(side_effect=mock_getMaxSpeed(4, 3, 5))
        position = car.beforeMove()
        self.assertEqual(position, (0, 1))
        # Best lane is the same speed as current.
        car = AutonomousCar(position=(0, 1), velocity=5, road=Mock())
        car._canChangeLane = Mock(return_value=True)
        car._shouldChangeLane = Mock(return_value=True)
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
