import unittest

import typing
from unittest.mock import Mock

from simulator.statistics.averageresult import AverageResult
from simulator.statistics.tracker import Tracker
from simulator.vehicle.car import Car
from simulator.vehicle.vehicle import Vehicle


class TrackerTestCase(unittest.TestCase):
    def test_trackVelocity(self):
        vehicles: typing.List[Vehicle] = [Mock(velocity=v) for v in range(10)]
        road = Mock()
        road.getAllActiveVehicles = lambda: vehicles
        tracker = Tracker(simulator=Mock(road=road))
        # No vehicles matching the predicate.
        result = tracker._trackVelocity(lambda _: False)
        expected = AverageResult(value=0, count=0)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))
        # All vehicles matching the predicate.
        result = tracker._trackVelocity(lambda _: True)
        expected = AverageResult(value=45, count=10)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

        # Some vehicles matching the predicate.
        def isEven(vehicle):
            return vehicle.velocity % 2 == 0

        result = tracker._trackVelocity(isEven)
        expected = AverageResult(value=20, count=5)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

    def test_trackThroughput(self):
        vehicles: typing.List[Vehicle] = [Mock(velocity=v) for v in range(10)]
        road = Mock(removed=vehicles)
        tracker = Tracker(simulator=Mock(road=road))
        # No vehicles matching the predicate.
        result = tracker._trackThroughput(lambda _: False)
        self.assertEqual(result, 0)
        # All vehicles matching the predicate.
        result = tracker._trackThroughput(lambda _: True)
        self.assertEqual(result, 10)

        # Some vehicles matching the predicate.
        def isEven(vehicle):
            return vehicle.velocity % 2 == 0

        result = tracker._trackThroughput(isEven)
        self.assertEqual(result, 5)

    def test_trackDecelerations(self):
        road = Mock()
        vehicles: typing.List[Vehicle] = []
        for velocity in range(10):
            vehicle = Mock(spec=Car)
            vehicle.velocity = velocity
            vehicle.path = [((0, 0), 12)]
            vehicles.append(vehicle)
        road.getAllActiveVehicles = lambda: vehicles
        tracker = Tracker(simulator=Mock(road=road))
        # No vehicles matching the predicate.
        result = tracker._trackDecelerations(lambda _: False)
        self.assertEqual(0, result)
        # All vehicles matching the predicate.
        result = tracker._trackDecelerations(lambda _: True)
        self.assertEqual(10, result)

        # Some vehicles matching the predicate.
        def isEven(vehicle: Vehicle) -> bool:
            return vehicle.velocity % 2 == 0

        result = tracker._trackDecelerations(isEven)
        self.assertEqual(5, result)

        # Test decelerations filter.
        road = Mock()
        vehicles: typing.List[Vehicle] = []
        # Vehicles which decelerated quickly.
        for _ in range(10):
            vehicle = Mock(spec=Car)
            vehicle.velocity = 5
            vehicle.path = [((0, 0), 10)]
            vehicles.append(vehicle)
        # Not cars, therefore should not be counted.
        for _ in range(10):
            vehicle = Mock(spec=Vehicle)
            vehicle.velocity = 5
            vehicle.path = [((0, 0), 10)]
            vehicles.append(vehicle)
        # Vehicles which did not decelerate quickly.
        for _ in range(10):
            vehicle = Mock(spec=Car)
            vehicle.velocity = 9
            vehicle.path = [((0, 0), 10)]
            vehicles.append(vehicle)
        road.getAllActiveVehicles = lambda: vehicles
        tracker = Tracker(simulator=Mock(road=road))
        result = tracker._trackDecelerations(lambda _: True)
        self.assertEqual(10, result)

    def test_trackLaneChanges(self):
        road = Mock()
        vehicles: typing.List[Vehicle] = []
        for x in range(10):
            vehicle = Mock()
            vehicle.position = (10 + x, 0)
            vehicle.last_position = (x, 1)
            vehicles.append(vehicle)
        road.getAllActiveVehicles = lambda: vehicles
        tracker = Tracker(simulator=Mock(road=road))
        # No vehicles matching the predicate.
        result = tracker._trackLaneChanges(lambda _: False)
        self.assertEqual(0, result)
        # All vehicles matching the predicate.
        result = tracker._trackLaneChanges(lambda _: True)
        self.assertEqual(10, result)

        # Some vehicles matching the predicate.
        def isEven(vehicle: Vehicle) -> bool:
            x, _ = vehicle.position
            return x % 2 == 0

        result = tracker._trackLaneChanges(isEven)
        self.assertEqual(5, result)

    def test_trackWaiting(self):
        road = Mock()
        vehicles: typing.List[Vehicle] = []
        for x in range(10):
            vehicle = Mock()
            vehicle.position = (x, 0)
            vehicle.last_position = (x, 0)
            vehicles.append(vehicle)
        road.getAllActiveVehicles = lambda: vehicles
        tracker = Tracker(simulator=Mock(road=road))
        # No vehicles matching the predicate.
        result = tracker._trackWaiting(lambda _: False)
        self.assertEqual(0, result)
        # All vehicles matching the predicate.
        result = tracker._trackWaiting(lambda _: True)
        self.assertEqual(10, result)

        # Some vehicles matching the predicate.
        def isEven(vehicle: Vehicle) -> bool:
            x, _ = vehicle.position
            return x % 2 == 0

        result = tracker._trackWaiting(isEven)
        self.assertEqual(5, result)


if __name__ == '__main__':
    unittest.main()
