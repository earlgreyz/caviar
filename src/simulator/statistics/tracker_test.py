import unittest

import typing
from unittest.mock import Mock

from simulator.statistics.averageresult import AverageResult
from simulator.statistics.filters import Filter
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

    def test_trackPercentage(self):
        road = Mock()
        vehicles: typing.List[Vehicle] = []
        for x in range(100):
            vehicles.append(Mock(position=(x, 0)))
        road.getAllActiveVehicles = lambda: vehicles
        tracker = Tracker(simulator=Mock(road=road))

        def make_filter(xfilter: typing.Callable[[int], bool]) -> Filter:
            def f(vehicle: Vehicle) -> bool:
                x, _ = vehicle.position
                return xfilter(x)

            return f

        no_filter = make_filter(lambda _: True)
        x50_filter = make_filter(lambda x: x < 50)
        x25_filter = make_filter(lambda x: x < 25)

        # Check count working.
        result = tracker._trackPercentage(x50_filter, no_filter)
        expected = AverageResult(value=50, count=50)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))
        # Check value working.
        result = tracker._trackPercentage(no_filter, x50_filter)
        expected = AverageResult(value=50, count=100)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))
        # More potential count than values.
        result = tracker._trackPercentage(x50_filter, x25_filter)
        expected = AverageResult(value=25, count=50)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))
        # More potential values than count.
        result = tracker._trackPercentage(x25_filter, x50_filter)
        expected = AverageResult(value=25, count=25)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

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
        expected = AverageResult(value=0, count=0)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))
        # All vehicles matching the predicate.
        result = tracker._trackDecelerations(lambda _: True)
        expected = AverageResult(value=10, count=10)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

        # Some vehicles matching the predicate.
        def isEven(vehicle: Vehicle) -> bool:
            return vehicle.velocity % 2 == 0

        result = tracker._trackDecelerations(isEven)
        expected = AverageResult(value=5, count=5)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

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
        expected = AverageResult(value=10, count=20)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

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
        expected = AverageResult(value=0, count=0)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))
        # All vehicles matching the predicate.
        result = tracker._trackLaneChanges(lambda _: True)
        expected = AverageResult(value=10, count=10)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

        # Some vehicles matching the predicate.
        def isEven(vehicle: Vehicle) -> bool:
            x, _ = vehicle.position
            return x % 2 == 0

        result = tracker._trackLaneChanges(isEven)
        expected = AverageResult(value=5, count=5)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

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
        expected = AverageResult(value=0, count=0)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))
        # All vehicles matching the predicate.
        result = tracker._trackWaiting(lambda _: True)
        expected = AverageResult(value=10, count=10)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

        # Some vehicles matching the predicate.
        def isEven(vehicle: Vehicle) -> bool:
            x, _ = vehicle.position
            return x % 2 == 0

        result = tracker._trackWaiting(isEven)
        expected = AverageResult(value=5, count=5)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))


if __name__ == '__main__':
    unittest.main()
