import typing
import unittest
from unittest.mock import Mock

from simulator.road.road import Road, CollisionError
from simulator.vehicle.vehicle import Vehicle


def implementsRoad(cls):
    assert hasattr(cls, 'getRoad') and callable(getattr(cls, 'getRoad'))

    def test_addVehicle(self: cls):
        # Add a vehicle.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (0, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # Try to add the vehicle outside the road length.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (100, 0)
        vehicle.position = position
        with self.assertRaises(IndexError):
            road.addVehicle(vehicle)
        # Try to add the vehicle outside the road lanes.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (0, 1)
        vehicle.position = position
        with self.assertRaises(IndexError):
            road.addVehicle(vehicle)
        # Try to add the vehicle to a nonempty road cell.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (0, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        another: Vehicle = Mock()
        another.position = position
        with self.assertRaises(CollisionError):
            road.addVehicle(another)

    def test_getVehicle(self: cls):
        # Add and retrieve the vehicle.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (0, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        result = road.getVehicle(position)
        self.assertEqual(result, vehicle, 'got invalid vehicle')
        # Get vehicle from an empty cell.
        road: Road = self.getRoad(length=100, lanes=1)
        position = (0, 0)
        result = road.getVehicle(position)
        self.assertIsNone(result, 'got unexpected vehicle')
        # Try to get vehicle from outside the road length.
        road: Road = self.getRoad(length=100, lanes=1)
        position = (100, 0)
        with self.assertRaises(IndexError):
            road.getVehicle(position)
        # Try to get the vehicle from outside the road lanes.
        road: Road = self.getRoad(length=100, lanes=1)
        position = (0, 1)
        with self.assertRaises(IndexError):
            road.getVehicle(position)

    def test_allVehicles(self: cls):
        # Add and retrieve all the vehicles from a single lane.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicles: typing.List[Vehicle] = []
        for i in range(100):
            vehicle: Vehicle = Mock()
            vehicle.position = (i, 0)
            vehicles.append(vehicle)
            road.addVehicle(vehicle)
        result = list(road.getAllVehicles())
        self.assertEqual(len(result), len(vehicles), 'got invalid number of vehicles')
        self.assertListEqual(result, list(reversed(vehicles)), 'vehicle lists differ')
        # Add and retrieve all the vehicles from multiple lanes.
        road: Road = self.getRoad(length=100, lanes=2)
        vehicles: typing.List[Vehicle] = []
        for lane in range(2):
            for x in range(100):
                vehicle: Vehicle = Mock()
                vehicle.position = (x, 1 - lane)
                vehicles.append(vehicle)
                road.addVehicle(vehicle)
        result = list(road.getAllVehicles())
        self.assertEqual(len(result), len(vehicles), 'got invalid number of vehicles')
        self.assertListEqual(result, list(reversed(vehicles)), 'vehicle lists differ')
        # Get vehicles from an empty road.
        road: Road = self.getRoad(length=100, lanes=2)
        result = list(road.getAllVehicles())
        self.assertEqual(len(result), 0, 'got invalid number of vehicles')
        self.assertListEqual(result, [], 'vehicle lists differ')

    def test_addPendingVehicle(self: cls):
        # Add a vehicle.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (0, 0)
        vehicle.position = position
        road.addPendingVehicle(vehicle)
        # Try to add the vehicle outside the road length.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (100, 0)
        vehicle.position = position
        with self.assertRaises(IndexError):
            road.addPendingVehicle(vehicle)
        # Try to add the vehicle outside the road lanes.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (0, 1)
        vehicle.position = position
        with self.assertRaises(IndexError):
            road.addPendingVehicle(vehicle)
        # Try to add the vehicle to a nonempty road cell.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (0, 0)
        vehicle.position = position
        road.addPendingVehicle(vehicle)
        another: Vehicle = Mock()
        another.position = position
        with self.assertRaises(CollisionError):
            road.addPendingVehicle(another)

    def test_getPendingVehicle(self: cls):
        # Add and retrieve the vehicle.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (0, 0)
        vehicle.position = position
        road.addPendingVehicle(vehicle)
        result = road.getPendingVehicle(position)
        self.assertEqual(result, vehicle, 'got invalid vehicle')
        # Get vehicle from an empty cell.
        road: Road = self.getRoad(length=100, lanes=1)
        position = (0, 0)
        result = road.getPendingVehicle(position)
        self.assertIsNone(result, 'got unexpected vehicle')
        # Try to get vehicle from outside the road length.
        road: Road = self.getRoad(length=100, lanes=1)
        position = (100, 0)
        with self.assertRaises(IndexError):
            road.getPendingVehicle(position)
        # Try to get the vehicle from outside the road lanes.
        road: Road = self.getRoad(length=100, lanes=1)
        position = (0, 1)
        with self.assertRaises(IndexError):
            road.getPendingVehicle(position)

    def test_getNextVehicle(self: cls):
        # Single lane.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (10, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # All positions < 10 should return the vehicle.
        for x in range(10):
            rx, result = road.getNextVehicle(position=(x, 0))
            self.assertEqual(rx, 10, f'got invalid next position x={x}')
            self.assertEqual(result, vehicle, f'got invalid next vehicle x={x}')
        # All positions >= 10 should return None.
        for x in range(10, 100):
            rx, result = road.getNextVehicle(position=(x, 0))
            self.assertEqual(rx, 100, f'got invalid next position x={x}')
            self.assertIsNone(result, f'got invalid next vehicle x={x}')
        # Multiple lanes.
        road: Road = self.getRoad(length=100, lanes=2)
        vehicle: Vehicle = Mock()
        position = (10, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # All positions < 10 should return the vehicle.
        for x in range(10):
            rx, result = road.getNextVehicle(position=(x, 0))
            self.assertEqual(rx, 10, f'got invalid next position x={x}')
            self.assertEqual(result, vehicle, f'got invalid next vehicle x={x}')
        # All positions >= 10 should return None.
        for x in range(10, 100):
            rx, result = road.getNextVehicle(position=(x, 0))
            self.assertEqual(rx, 100, f'got invalid next position x={x}')
            self.assertIsNone(result, f'got invalid next vehicle x={x}')
        for x in range(100):
            rx, result = road.getNextVehicle(position=(x, 1))
            self.assertEqual(rx, 100, f'got invalid next position for x={x}')
            self.assertIsNone(result, f'got invalid next vehicle for x={x}')
        # Check errors.
        road: Road = self.getRoad(length=100, lanes=1)
        with self.assertRaises(IndexError):
            road.getNextVehicle(position=(-1, 0))
        with self.assertRaises(IndexError):
            road.getNextVehicle(position=(100, 0))
        with self.assertRaises(IndexError):
            road.getNextVehicle(position=(0, 1))
        with self.assertRaises(IndexError):
            road.getNextVehicle(position=(0, -1))

    def test_getPreviousVehicle(self: cls):
        # Single lane.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (90, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # All positions <= 90 should return None.
        for x in range(91):
            rx, result = road.getPreviousVehicle(position=(x, 0))
            self.assertEqual(rx, -1, f'got invalid previous position x={x}')
            self.assertIsNone(result, f'got invalid previous vehicle x={x}')
        # All positions > 90 should return the vehicle.
        for x in range(91, 100):
            rx, result = road.getPreviousVehicle(position=(x, 0))
            self.assertEqual(rx, 90, f'got invalid previous position x={x}')
            self.assertEqual(result, vehicle, f'got invalid previous vehicle x={x}')
        # Multiple lanes.
        road: Road = self.getRoad(length=100, lanes=2)
        vehicle: Vehicle = Mock()
        position = (90, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # All positions <= 90 should return None.
        for x in range(91):
            rx, result = road.getPreviousVehicle(position=(x, 0))
            self.assertEqual(rx, -1, f'got invalid previous position x={x}')
            self.assertIsNone(result, f'got invalid previous vehicle x={x}')
        # All positions > 90 should return the vehicle.
        for x in range(91, 100):
            rx, result = road.getPreviousVehicle(position=(x, 0))
            self.assertEqual(rx, 90, f'got invalid previous position x={x}')
            self.assertEqual(result, vehicle, f'got invalid previous vehicle x={x}')
        for x in range(100):
            rx, result = road.getPreviousVehicle(position=(x, 1))
            self.assertEqual(rx, -1, f'got invalid previous position x={x}')
            self.assertIsNone(result, f'got invalid previous vehicle x={x}')
        # Check errors.
        road: Road = self.getRoad(length=100, lanes=1)
        with self.assertRaises(IndexError):
            road.getPreviousVehicle(position=(-1, 0))
        with self.assertRaises(IndexError):
            road.getPreviousVehicle(position=(100, 0))
        with self.assertRaises(IndexError):
            road.getPreviousVehicle(position=(0, 1))
        with self.assertRaises(IndexError):
            road.getPreviousVehicle(position=(0, -1))

    def test_commitLanes(self: cls):
        road: Road = self.getRoad(length=100, lanes=1)
        vehicles: typing.List[Vehicle] = []
        for x in range(100):
            vehicle = Mock()
            vehicle.position = (x, 0)
            vehicles.append(vehicle)
            road.addPendingVehicle(vehicle)
        road._commitLanes()
        for x in range(100):
            result = road.getVehicle(position=(x, 0))
            self.assertEqual(result, vehicles[x], f'got invalid vehicle x={x}')

    def test_updateLanes(self: cls):
        road: Road = self.getRoad(length=100, lanes=1)
        vehicles: typing.List[Vehicle] = []
        for x in range(100):
            vehicle = Mock()
            vehicle.position = (x, 0)
            vehicles.append(vehicle)
            road.addVehicle(vehicle)

        # Check if updateLanes traverses all vehicles.
        def f(vehicle):
            return vehicle.position

        road._updateLanes(f)
        self.assertCountEqual(road.getAllVehicles(), vehicles, 'not all vehicles were traversed')

        # Check if vehicles outside of the road are removed.
        def g(vehicle):
            x, lane = vehicle.position
            vehicle.position = x + 5, lane
            return vehicle.position

        road._updateLanes(g)
        self.assertCountEqual(road.getAllVehicles(), vehicles[:-5], 'vehicles not removed')

    cls.test_addVehicle = test_addVehicle
    cls.test_getVehicle = test_getVehicle
    cls.test_allVehicles = test_allVehicles
    cls.test_addPendingVehicle = test_addPendingVehicle
    cls.test_getNextVehicle = test_getNextVehicle
    cls.test_getPreviousVehicle = test_getPreviousVehicle
    cls.test_commitLanes = test_commitLanes
    cls.test_updateLanes = test_updateLanes
    return cls


class RoadTestCase(unittest.TestCase):
    def test_interface(self):
        road = Road(100, 1)
        with self.assertRaises(NotImplementedError):
            road.addVehicle(vehicle=Mock())
        with self.assertRaises(NotImplementedError):
            _ = road.getVehicle(position=(0, 0))
        with self.assertRaises(NotImplementedError):
            _ = road.getAllVehicles()
        with self.assertRaises(NotImplementedError):
            road.addPendingVehicle(vehicle=Mock())
        with self.assertRaises(NotImplementedError):
            _ = road.getPendingVehicle(position=(0, 0))
        with self.assertRaises(NotImplementedError):
            _ = road.getNextVehicle(position=(0, 0))
        with self.assertRaises(NotImplementedError):
            _ = road.getPreviousVehicle(position=(0, 0))
        with self.assertRaises(NotImplementedError):
            _ = road._commitLanes()

    def test_isProperPosition(self):
        road = Road(100, 1)
        self.assertTrue(road.isProperPosition(position=(0, 0)))
        self.assertTrue(road.isProperPosition(position=(99, 0)))
        self.assertFalse(road.isProperPosition(position=(-1, 0)))
        self.assertFalse(road.isProperPosition(position=(100, 0)))
        self.assertFalse(road.isProperPosition(position=(0, 1)))
        self.assertFalse(road.isProperPosition(position=(0, -1)))

    def test_getAverageVelocityFiltered(self):
        road = Road(100, 1)
        vehicles: typing.List[Vehicle] = []
        for velocity in range(10):
            vehicle = Mock()
            vehicle.velocity = velocity
            vehicles.append(vehicle)
        road.getAllVehicles = lambda: vehicles
        # No vehicles matching the predicate.
        self.assertEqual(road.getAverageVelocityFiltered(lambda _: False), 0, 'invalid velocity')
        # All vehicles matching the predicate.
        self.assertEqual(road.getAverageVelocityFiltered(lambda _: True), 4.5, 'invalid velocity')

        # Some vehicles matching the predicate.
        def isEven(vehicle):
            return vehicle.velocity % 2 == 0

        self.assertEqual(road.getAverageVelocityFiltered(isEven), 4.0, 'invalid velocity')

    def test_getAverageVelocity(self):
        road = Road(100, 1)
        vehicles: typing.List[Vehicle] = []
        for velocity in range(10):
            vehicle = Mock()
            vehicle.velocity = velocity
            vehicles.append(vehicle)
        road.getAllVehicles = lambda: vehicles
        self.assertEqual(road.getAverageVelocity(), 4.5, 'invalid velocity')

    def test_step(self):
        road = Road(100, 1)
        vehicle = Mock()
        road._updateLanes = lambda f: f(vehicle)
        road.step()
        vehicle.beforeMove.assert_called_once()
        vehicle.move.assert_called_once()


if __name__ == '__main__':
    unittest.main()
