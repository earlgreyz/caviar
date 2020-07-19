import typing
import unittest
from unittest.mock import Mock

from simulator.position import Position
from simulator.vehicle.car import Car, isCar
from simulator.vehicle.vehicle import Vehicle


class CarTestCase(unittest.TestCase):
    def test_getMaxSpeedUnlimited(self):
        road = Mock(length=100)
        road.controller = Mock()
        road.controller.getMaxSpeed.return_value = 5
        car = Car(position=(0, 0), velocity=5, road=road)
        # No vehicles in front.
        road.getNextVehicle.return_value = (100, None)
        limit = car._getMaxSpeedUnlimited(position=(0, 0))
        self.assertEqual(limit, 100)
        # Vehicle in front is far away.
        road.getNextVehicle.return_value = (10, Mock())
        limit = car._getMaxSpeedUnlimited(position=(0, 0))
        self.assertEqual(limit, 9)
        # Vehicle in front is blocking the road.
        road.getNextVehicle.return_value = (2, Mock())
        limit = car._getMaxSpeedUnlimited(position=(0, 0))
        self.assertEqual(limit, 1)

    def test_getMaxSpeed(self):
        road = Mock(length=100)
        road.controller = Mock()
        road.controller.getMaxSpeed.return_value = 5
        car = Car(position=(0, 0), velocity=5, road=road)
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

    def test_isChangeRequired(self):
        road = Mock()
        car = Car(position=(0, 0), velocity=1, length=1, road=road)
        car._getMaxSpeedUnlimited = Mock(return_value=1)
        self.assertTrue(car._isChangeRequired())
        car._getMaxSpeedUnlimited = Mock(return_value=5)
        self.assertFalse(car._isChangeRequired())

    def test_isChangePossible(self):
        road = Mock()

        def mock_isSafePosition(invalid: typing.List[Position]) \
                -> typing.Callable[[Position], bool]:
            return lambda position: position not in invalid

        # Vehicle of one cell length .
        car = Car(position=(0, 0), velocity=1, length=1, road=road)
        road.isSafePosition.side_effect = mock_isSafePosition([])
        self.assertTrue(car._isChangePossible(destination=(0, 1)))
        road.isSafePosition.side_effect = mock_isSafePosition([(0, 1)])
        self.assertFalse(car._isChangePossible(destination=(0, 1)))
        # Longer vehicle.
        car = Car(position=(3, 0), velocity=1, length=3, road=road)
        road.isSafePosition.side_effect = mock_isSafePosition([(3, 1)])
        self.assertFalse(car._isChangePossible(destination=(3, 1)))
        road.isSafePosition.side_effect = mock_isSafePosition([(2, 1)])
        self.assertFalse(car._isChangePossible(destination=(3, 1)))
        road.isSafePosition.side_effect = mock_isSafePosition([(1, 1)])
        self.assertFalse(car._isChangePossible(destination=(3, 1)))
        road.isSafePosition.side_effect = mock_isSafePosition([(0, 1)])
        self.assertTrue(car._isChangePossible(destination=(3, 1)))

    def test_isChangeBeneficial(self):
        road = Mock()
        car = Car(position=(0, 0), velocity=5, length=3, road=road)
        # Same speed.
        car._getMaxSpeedUnlimited = Mock(return_value=5)
        car.velocity = 5
        self.assertFalse(car._isChangeBeneficial(destination=(0, 1)))
        # Lower speed.
        car._getMaxSpeedUnlimited = Mock(return_value=4)
        car.velocity = 5
        self.assertFalse(car._isChangeBeneficial(destination=(0, 1)))
        # Higher speed.
        car._getMaxSpeedUnlimited = Mock(return_value=5)
        car.velocity = 3
        self.assertTrue(car._isChangeBeneficial(destination=(0, 1)))

    def test_isChangeSafe(self):
        # Test parameters.
        x = 42
        max_speed = 5
        length = 3

        road = Mock()
        road.controller = Mock()
        road.controller.getMaxSpeed.return_value = max_speed
        car = Car(position=(x, 0), velocity=1, length=length, road=road)
        # No vehicle behind.
        road.getPreviousVehicle.return_value = -1, None
        self.assertTrue(car._isChangeSafe(destination=(x, 1)))
        # Previous vehicle is far.
        road.getPreviousVehicle.return_value = 0, Mock()
        self.assertTrue(car._isChangeSafe(destination=(x, 1)))
        # Previous vehicle overlaps with the car.
        for i in range(max_speed + length):
            road.getPreviousVehicle.return_value = x - i, Mock()
            self.assertFalse(car._isChangeSafe(destination=(x, 1)))
        road.getPreviousVehicle.return_value = x - max_speed - length, Mock()
        self.assertTrue(car._isChangeSafe(destination=(x, 1)))

    def test_changeLane(self):
        car = Car(position=(0, 0), velocity=1, length=3, road=Mock())
        for r in (True, False):
            car._isChangeRequired = Mock(return_value=r)
            for p in (True, False):
                car._isChangePossible = Mock(return_value=p)
                for b in (True, False):
                    car._isChangeBeneficial = Mock(return_value=b)
                    for s in (True, False):
                        car._isChangeSafe = Mock(return_value=s)
                        # Only true when all conditions are met.
                        if r and p and b and s:
                            self.assertTrue(car._changeLane(destination=(0, 1)))
                        else:
                            self.assertFalse(car._changeLane(destination=(0, 1)))

    def test_isAutonomous(self):
        car = Car(position=(0, 0), velocity=1, road=Mock())
        self.assertTrue(isCar(car))
        vehicle = Vehicle(position=(0, 0), velocity=0)
        self.assertFalse(isCar(vehicle))


if __name__ == '__main__':
    unittest.main()
