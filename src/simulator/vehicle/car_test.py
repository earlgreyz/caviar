import typing
import unittest
from unittest.mock import Mock

from simulator.position import Position
from simulator.vehicle.car import Car


class CarTestCase(unittest.TestCase):
    def test_getMaxSpeed(self):
        road = Mock()
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
        car = Car(position=(0, 0), velocity=1, length=3, road=road)
        max_speed = {}
        car._getMaxSpeed = Mock(side_effect=lambda position: max_speed.get(position))
        # Same speed.
        max_speed[(0, 0)] = 5
        max_speed[(0, 1)] = 5
        self.assertFalse(car._isChangeBeneficial(destination=(0, 1)))
        # Lower speed.
        max_speed[(0, 0)] = 5
        max_speed[(0, 1)] = 4
        self.assertFalse(car._isChangeBeneficial(destination=(0, 1)))
        # Higher speed.
        max_speed[(0, 0)] = 4
        max_speed[(0, 1)] = 5
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
        possible = [False, False, False, False, True, True, True]
        beneficial = [False, False, True, True, False, False, True]
        safe = [False, True, False, True, False, True, False]
        for p, b, s in zip(possible, beneficial, safe):
            car._isChangePossible = Mock(return_value=p)
            car._isChangeBeneficial = Mock(return_value=b)
            car._isChangeSafe = Mock(return_value=s)
            self.assertFalse(car._changeLane(destination=(0, 1)))
        # Change possible.
        car._isChangePossible = Mock(return_value=True)
        car._isChangeBeneficial = Mock(return_value=True)
        car._isChangeSafe = Mock(return_value=True)
        self.assertTrue(car._changeLane(destination=(0, 1)))


if __name__ == '__main__':
    unittest.main()
