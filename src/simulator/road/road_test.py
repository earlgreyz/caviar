import typing
import unittest
from unittest.mock import Mock, call
from itertools import chain, combinations

from simulator.position import Position
from simulator.road.road import Road, CollisionError
from simulator.vehicle.vehicle import Vehicle, VehicleFlags


def implementsRoad(cls):
    assert hasattr(cls, 'getRoad') and callable(getattr(cls, 'getRoad'))

    def test_addVehicle(self: cls):
        # Add a vehicle.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (0, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # Try to add the vehicle outside the road length.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (100, 0)
        vehicle.position = position
        with self.assertRaises(IndexError):
            road.addVehicle(vehicle)
        # Try to add the vehicle outside the road lanes.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (0, 1)
        vehicle.position = position
        with self.assertRaises(IndexError):
            road.addVehicle(vehicle)
        # Try to add the vehicle to a nonempty road cell.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (0, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        another: Vehicle = Mock(length=1, width=1)
        another.position = position
        with self.assertRaises(CollisionError):
            road.addVehicle(another)

    def test_addVehicle__length(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=2, width=1)
        position = (1, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        result = road.getVehicle(position)
        self.assertEqual(result, vehicle)
        result = road.getVehicle((0, 0))
        self.assertEqual(result, vehicle)
        result = road.getVehicle((2, 0))
        self.assertIsNone(result)

    def test_addVehicle__width(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=2)
        vehicle: Vehicle = Mock(length=1, width=1)
        vehicle.position = (0, 1)
        road.addVehicle(vehicle)
        another: Vehicle = Mock(length=1, width=2)
        another.position = (0, 0)
        with self.assertRaises(CollisionError):
            road.addVehicle(another)

    def test_getVehicle(self: cls):
        # Add and retrieve the vehicle.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (0, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        result = road.getVehicle(position)
        self.assertEqual(result, vehicle)
        # Get vehicle from an empty cell.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        position = (0, 0)
        result = road.getVehicle(position)
        self.assertIsNone(result)
        # Try to get vehicle from outside the road length.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        position = (100, 0)
        with self.assertRaises(IndexError):
            road.getVehicle(position)
        # Try to get the vehicle from outside the road lanes.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        position = (0, 1)
        with self.assertRaises(IndexError):
            road.getVehicle(position)

    def test_getVehicle__length(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=5, width=1)
        position = (4, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        for x in range(5):
            result = road.getVehicle(position=(x, 0))
            self.assertEqual(result, vehicle, f'invalid vehicle x={x}')

    def test_getVehicle__width(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=2)
        vehicle: Vehicle = Mock(length=1, width=2)
        position = (0, 1)
        vehicle.position = position
        road.addVehicle(vehicle)
        for w in range(1, 3):
            result = road.getVehicle(position=(0, w))
            self.assertEqual(result, vehicle, f'invalid vehicle w={w}')

    def test_getAllVehicles(self: cls):
        # Add and retrieve all the vehicles from a single lane.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicles: typing.List[Vehicle] = []
        for i in range(100):
            vehicle: Vehicle = Mock(length=1, width=1)
            vehicle.position = (i, 0)
            vehicles.append(vehicle)
            road.addVehicle(vehicle)
        result = list(road.getAllVehicles())
        self.assertEqual(len(result), len(vehicles))
        self.assertListEqual(result, list(reversed(vehicles)))
        # Add and retrieve all the vehicles from multiple lanes.
        road: Road = self.getRoad(length=100, lanes=2, width=1)
        vehicles: typing.List[Vehicle] = []
        for lane in range(2):
            for x in range(100):
                vehicle: Vehicle = Mock(length=1, width=1)
                vehicle.position = (x, 1 - lane)
                vehicles.append(vehicle)
                road.addVehicle(vehicle)
        result = list(road.getAllVehicles())
        self.assertEqual(len(result), len(vehicles))
        self.assertListEqual(result, list(reversed(vehicles)))
        # Get vehicles from an empty road.
        road: Road = self.getRoad(length=100, lanes=2, width=1)
        result = list(road.getAllVehicles())
        self.assertEqual(len(result), 0)
        self.assertListEqual(result, [])

    def test_getAllVehicles__length(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicles: typing.List[Vehicle] = []
        for i in range(1, 100, 2):
            vehicle: Vehicle = Mock(length=2, width=1)
            vehicle.position = (i, 0)
            vehicles.append(vehicle)
            road.addVehicle(vehicle)
        result = list(road.getAllVehicles())
        self.assertEqual(len(result), len(vehicles))
        self.assertListEqual(result, list(reversed(vehicles)))

    def test_getAllVehicles__width(self: cls):
        road: Road = self.getRoad(length=100, lanes=2, width=2)
        vehicles: typing.List[Vehicle] = []
        for i in range(1, 100, 2):
            vehicle: Vehicle = Mock(length=2, width=2)
            vehicle.position = (i, 0)
            vehicles.append(vehicle)
            road.addVehicle(vehicle)
        result = list(road.getAllVehicles())
        self.assertEqual(len(result), len(vehicles))
        self.assertListEqual(result, list(reversed(vehicles)))

    def test_addPendingVehicle(self: cls):
        # Add a vehicle.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (0, 0)
        vehicle.position = position
        road.addPendingVehicle(vehicle)
        # Try to add the vehicle outside the road length.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (100, 0)
        vehicle.position = position
        with self.assertRaises(IndexError):
            road.addPendingVehicle(vehicle)
        # Try to add the vehicle outside the road lanes.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (0, 1)
        vehicle.position = position
        with self.assertRaises(IndexError):
            road.addPendingVehicle(vehicle)
        # Try to add the vehicle to a nonempty road cell.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (0, 0)
        vehicle.position = position
        road.addPendingVehicle(vehicle)
        another: Vehicle = Mock(length=1, width=1)
        another.position = position
        with self.assertRaises(CollisionError):
            road.addPendingVehicle(another)

    def test_addPendingVehicle__length(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=2, width=1)
        position = (1, 0)
        vehicle.position = position
        road.addPendingVehicle(vehicle)
        result = road.getPendingVehicle(position)
        self.assertEqual(result, vehicle)
        result = road.getPendingVehicle((0, 0))
        self.assertEqual(result, vehicle)
        result = road.getPendingVehicle((2, 0))
        self.assertIsNone(result)

    def test_addPendingVehicle__width(self: cls):
        # Lane is not fully empty.
        road: Road = self.getRoad(length=100, lanes=1, width=2)
        vehicle: Vehicle = Mock(length=1, width=1)
        vehicle.position = (0, 1)
        road.addPendingVehicle(vehicle)
        another: Vehicle = Mock(length=1, width=2)
        another.position = (0, 0)
        with self.assertRaises(CollisionError):
            road.addPendingVehicle(another)

    def test_getPendingVehicle(self: cls):
        # Add and retrieve the vehicle.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (0, 0)
        vehicle.position = position
        road.addPendingVehicle(vehicle)
        result = road.getPendingVehicle(position)
        self.assertEqual(result, vehicle)
        # Get vehicle from an empty cell.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        position = (0, 0)
        result = road.getPendingVehicle(position)
        self.assertIsNone(result)
        # Try to get vehicle from outside the road length.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        position = (100, 0)
        with self.assertRaises(IndexError):
            road.getPendingVehicle(position)
        # Try to get the vehicle from outside the road lanes.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        position = (0, 1)
        with self.assertRaises(IndexError):
            road.getPendingVehicle(position)

    def test_getPendingVehicle__length(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=5, width=1)
        position = (4, 0)
        vehicle.position = position
        road.addPendingVehicle(vehicle)
        for x in range(5):
            result = road.getPendingVehicle(position=(x, 0))
            self.assertEqual(result, vehicle, f'invalid vehicle x={x}')

    def test_getPendingVehicle__width(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=2)
        vehicle: Vehicle = Mock(length=1, width=2)
        position = (0, 1)
        vehicle.position = position
        road.addPendingVehicle(vehicle)
        for w in range(1, 3):
            result = road.getPendingVehicle(position=(0, w))
            self.assertEqual(result, vehicle, f'invalid vehicle w={w}')

    def test_getNextVehicle(self: cls):
        # Single lane.
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (10, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # All positions < 10 should return the vehicle.
        for x in range(10):
            rx, result = road.getNextVehicle(position=(x, 0))
            self.assertEqual(rx, 10, f'invalid next position x={x}')
            self.assertEqual(result, vehicle, f'invalid next vehicle x={x}')
        # All positions >= 10 should return None.
        for x in range(10, 100):
            rx, result = road.getNextVehicle(position=(x, 0))
            self.assertEqual(rx, 100, f'invalid next position x={x}')
            self.assertIsNone(result, f'invalid next vehicle x={x}')
        # Multiple lanes.
        road: Road = self.getRoad(length=100, lanes=2, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (10, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # All positions < 10 should return the vehicle.
        for x in range(10):
            rx, result = road.getNextVehicle(position=(x, 0))
            self.assertEqual(rx, 10, f'invalid next position x={x}')
            self.assertEqual(result, vehicle, f'invalid next vehicle x={x}')
        # All positions >= 10 should return None.
        for x in range(10, 100):
            rx, result = road.getNextVehicle(position=(x, 0))
            self.assertEqual(rx, 100, f'invalid next position x={x}')
            self.assertIsNone(result, f'invalid next vehicle x={x}')
        for x in range(100):
            rx, result = road.getNextVehicle(position=(x, 1))
            self.assertEqual(rx, 100, f'invalid next position for x={x}')
            self.assertIsNone(result, f'invalid next vehicle for x={x}')

    def test_getNextVehicle__length(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=5, width=1)
        position = (10, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # All positions < 5 should return the vehicle at its starting position.
        for x in range(5):
            rx, result = road.getNextVehicle(position=(x, 0))
            self.assertEqual(rx, 6, f'invalid next position x={x}')
            self.assertEqual(result, vehicle, f'invalid next vehicle x={x}')
        # All positions < 10 should return the vehicle at its closest position.
        for x in range(6, 10):
            rx, result = road.getNextVehicle(position=(x, 0))
            self.assertEqual(rx, x + 1, f'invalid next position x={x}')
            self.assertEqual(result, vehicle, f'invalid next vehicle x={x}')
        # All positions >= 10 should return None.
        for x in range(10, 100):
            rx, result = road.getNextVehicle(position=(x, 0))
            self.assertEqual(rx, 100, f'invalid next position x={x}')
            self.assertIsNone(result, f'invalid next vehicle x={x}')

    def test_getNextVehicle__width(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=2)
        vehicle: Vehicle = Mock(length=1, width=2)
        position = (10, 1)
        vehicle.position = position
        road.addVehicle(vehicle)
        # All positions < 10 should return the vehicle on both sub-lanes.
        for x in range(10):
            rx, result = road.getNextVehicle(position=(x, 1))
            self.assertEqual(rx, 10, f'invalid next position x={x}')
            self.assertEqual(result, vehicle, f'invalid next vehicle x={x}')
            rx, result = road.getNextVehicle(position=(x, 2))
            self.assertEqual(rx, 10, f'invalid next position x={x}')
            self.assertEqual(result, vehicle, f'invalid next vehicle x={x}')
        # All positions >= 10 should return None on both sub-lanes.
        for x in range(10, 100):
            rx, result = road.getNextVehicle(position=(x, 1))
            self.assertEqual(rx, 100, f'invalid next position x={x}')
            self.assertIsNone(result, f'invalid next vehicle x={x}')
            rx, result = road.getNextVehicle(position=(x, 2))
            self.assertEqual(rx, 100, f'invalid next position x={x}')
            self.assertIsNone(result, f'invalid next vehicle x={x}')

    def test_getNextVehicle__errors(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=1)
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
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (90, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # All positions <= 90 should return None.
        for x in range(91):
            rx, result = road.getPreviousVehicle(position=(x, 0))
            self.assertEqual(rx, -1, f'invalid previous position x={x}')
            self.assertIsNone(result, f'invalid previous vehicle x={x}')
        # All positions > 90 should return the vehicle.
        for x in range(91, 100):
            rx, result = road.getPreviousVehicle(position=(x, 0))
            self.assertEqual(rx, 90, f'invalid previous position x={x}')
            self.assertEqual(result, vehicle, f'invalid previous vehicle x={x}')
        # Multiple lanes.
        road: Road = self.getRoad(length=100, lanes=2, width=1)
        vehicle: Vehicle = Mock(length=1, width=1)
        position = (90, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # All positions <= 90 should return None.
        for x in range(91):
            rx, result = road.getPreviousVehicle(position=(x, 0))
            self.assertEqual(rx, -1, f'invalid previous position x={x}')
            self.assertIsNone(result, f'invalid previous vehicle x={x}')
        # All positions > 90 should return the vehicle.
        for x in range(91, 100):
            rx, result = road.getPreviousVehicle(position=(x, 0))
            self.assertEqual(rx, 90, f'invalid previous position x={x}')
            self.assertEqual(result, vehicle, f'invalid previous vehicle x={x}')
        for x in range(100):
            rx, result = road.getPreviousVehicle(position=(x, 1))
            self.assertEqual(rx, -1, f'invalid previous position x={x}')
            self.assertIsNone(result, f'invalid previous vehicle x={x}')

    def test_getPreviousVehicle__length(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicle: Vehicle = Mock(length=5, width=1)
        position = (90, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # All positions <= 87 should return None.
        for x in range(87):
            rx, result = road.getPreviousVehicle(position=(x, 0))
            self.assertEqual(rx, -1, f'invalid previous position x={x}')
            self.assertIsNone(result, f'invalid previous vehicle x={x}')
        # All positions > 87 should return the vehicle at its closest position.
        for x in range(87, 91):
            rx, result = road.getPreviousVehicle(position=(x, 0))
            self.assertEqual(rx, x - 1, f'invalid previous position x={x}')
            self.assertEqual(result, vehicle, f'invalid previous vehicle x={x}')
        # All positions > 90 should return the vehicle at its starting position.
        for x in range(91, 100):
            rx, result = road.getPreviousVehicle(position=(x, 0))
            self.assertEqual(rx, 90, f'invalid previous position x={x}')
            self.assertEqual(result, vehicle, f'invalid previous vehicle x={x}')

    def test_getPreviousVehicle__width(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=2)
        vehicle: Vehicle = Mock(length=1, width=2)
        position = (90, 1)
        vehicle.position = position
        road.addVehicle(vehicle)
        # All positions <= 90 should return None on both sub-lanes.
        for x in range(91):
            rx, result = road.getPreviousVehicle(position=(x, 1))
            self.assertEqual(rx, -1, f'invalid previous position x={x}')
            self.assertIsNone(result, f'invalid previous vehicle x={x}')
            rx, result = road.getPreviousVehicle(position=(x, 2))
            self.assertEqual(rx, -1, f'invalid previous position x={x}')
            self.assertIsNone(result, f'invalid previous vehicle x={x}')
        # All positions > 90 should return the vehicle on both sub-lanes.
        for x in range(91, 100):
            rx, result = road.getPreviousVehicle(position=(x, 1))
            self.assertEqual(rx, 90, f'invalid previous position x={x}')
            self.assertEqual(result, vehicle, f'invalid previous vehicle x={x}')
            rx, result = road.getPreviousVehicle(position=(x, 2))
            self.assertEqual(rx, 90, f'invalid previous position x={x}')
            self.assertEqual(result, vehicle, f'invalid previous vehicle x={x}')

    def test_getPreviousVehicle__errors(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        with self.assertRaises(IndexError):
            road.getPreviousVehicle(position=(-1, 0))
        with self.assertRaises(IndexError):
            road.getPreviousVehicle(position=(100, 0))
        with self.assertRaises(IndexError):
            road.getPreviousVehicle(position=(0, 1))
        with self.assertRaises(IndexError):
            road.getPreviousVehicle(position=(0, -1))

    def test_commitLanes(self: cls):
        road: Road = self.getRoad(length=100, lanes=1, width=1)
        vehicles: typing.List[Vehicle] = []
        for x in range(100):
            vehicle = Mock(length=1, width=1)
            vehicle.position = (x, 0)
            vehicles.append(vehicle)
            road.addPendingVehicle(vehicle)
        road._commitLanes()
        for x in range(100):
            result = road.getVehicle(position=(x, 0))
            self.assertEqual(result, vehicles[x], f'invalid vehicle x={x}')

    def test_updateLanes(self: cls):
        road: Road = self.getRoad(length=10, lanes=1, width=1)
        vehicles: typing.List[Vehicle] = []
        for x in range(10):
            vehicle = Mock(length=1, width=1, flags=VehicleFlags.NONE)
            vehicle.position = (x, 0)
            vehicles.append(vehicle)
            road.addVehicle(vehicle)

        # Check if updateLanes traverses all vehicles.
        result: typing.List[Vehicle] = []

        def f(vehicle):
            result.append(vehicle)
            return vehicle.position

        road._updateLanes(f)
        self.assertCountEqual(result, vehicles, 'not all vehicles were traversed')

        # Check if vehicles outside of the road are removed.
        def g(vehicle):
            x, lane = vehicle.position
            vehicle.position = x + 5, lane
            return vehicle.position

        road._updateLanes(g)
        self.assertCountEqual(road.getAllVehicles(), vehicles[:-5], 'vehicles not removed')
        self.assertCountEqual(road.removed, vehicles[-5:], 'invalid vehicles removed')

    def test_updateLanes__length(self: cls):
        road: Road = self.getRoad(length=10, lanes=1, width=1)
        vehicles: typing.List[Vehicle] = []
        for i in range(1, 10, 2):
            vehicle: Vehicle = Mock(length=2, width=1, flags=VehicleFlags.NONE)
            vehicle.position = (i, 0)
            vehicles.append(vehicle)
            road.addVehicle(vehicle)

        # Check if updateLanes traverses all vehicles once.
        result: typing.List[Vehicle] = []

        def f(vehicle):
            result.append(vehicle)
            return vehicle.position

        road._updateLanes(f)
        self.assertCountEqual(result, vehicles, 'not all vehicles were traversed')

    def test_updateLanes__width(self: cls):
        road: Road = self.getRoad(length=10, lanes=1, width=2)
        vehicles: typing.List[Vehicle] = []
        for i in range(1, 10, 2):
            vehicle: Vehicle = Mock(length=1, width=2, flags=VehicleFlags.NONE)
            vehicle.position = (i, 1)
            vehicles.append(vehicle)
            road.addVehicle(vehicle)

        # Check if updateLanes traverses all vehicles once.
        result: typing.List[Vehicle] = []

        def f(vehicle):
            result.append(vehicle)
            return vehicle.position

        road._updateLanes(f)
        self.assertCountEqual(result, vehicles, 'not all vehicles were traversed')

    cls.test_addVehicle = test_addVehicle
    cls.test_addVehicle__length = test_addVehicle__length
    cls.test_addVehicle__width = test_addVehicle__width
    cls.test_getVehicle = test_getVehicle
    cls.test_getVehicle__length = test_getVehicle__length
    cls.test_getVehicle__width = test_getVehicle__width
    cls.test_getAllVehicles = test_getAllVehicles
    cls.test_getAllVehicles__length = test_getAllVehicles__length
    cls.test_getAllVehicles__width = test_getAllVehicles__width
    cls.test_addPendingVehicle = test_addPendingVehicle
    cls.test_addPendingVehicle__length = test_addPendingVehicle__length
    cls.test_addPendingVehicle__width = test_addPendingVehicle__width
    cls.test_getPendingVehicle = test_getPendingVehicle
    cls.test_getPendingVehicle__length = test_getPendingVehicle__length
    cls.test_getPendingVehicle__width = test_getPendingVehicle__width
    cls.test_getNextVehicle = test_getNextVehicle
    cls.test_getNextVehicle__length = test_getNextVehicle__length
    cls.test_getNextVehicle__width = test_getNextVehicle__width
    cls.test_getNextVehicle__errors = test_getNextVehicle__errors
    cls.test_getPreviousVehicle = test_getPreviousVehicle
    cls.test_getPreviousVehicle__length = test_getPreviousVehicle__length
    cls.test_getPreviousVehicle__width = test_getPreviousVehicle__width
    cls.test_getPreviousVehicle__errors = test_getPreviousVehicle__errors
    cls.test_commitLanes = test_commitLanes
    cls.test_updateLanes = test_updateLanes
    cls.test_updateLanes__length = test_updateLanes__length
    cls.test_updateLanes__width = test_updateLanes__width
    return cls


class RoadTestCase(unittest.TestCase):
    def test_interface(self):
        road = Road(100, 1, 1)
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

    def test_sublanesCount(self):
        road = Road(100, 1, lane_width=1)
        self.assertEqual(road.sublanesCount, 1)
        road = Road(100, 2, lane_width=1)
        self.assertEqual(road.sublanesCount, 2)
        road = Road(100, 1, lane_width=2)
        self.assertEqual(road.sublanesCount, 4)
        road = Road(100, 2, lane_width=2)
        self.assertEqual(road.sublanesCount, 6)
        road = Road(100, 1, lane_width=4)
        self.assertEqual(road.sublanesCount, 8)
        road = Road(100, 2, lane_width=4)
        self.assertEqual(road.sublanesCount, 12)

    def test_getRelativePosition(self):
        road = Road(100, 2, lane_width=1)
        for x in range(100):
            for lane in range(2):
                position = (x, lane)
                result = road.getRelativePosition(position=position)
                self.assertEqual(result, position, f'invalid position for ({x}, {lane})')
        road = Road(100, 2, lane_width=2)
        self.assertEqual(road.getRelativePosition((0, 0)), (0, 1))
        self.assertEqual(road.getRelativePosition((42, 0)), (42, 1))
        self.assertEqual(road.getRelativePosition((0, 1)), (0, 3))
        self.assertEqual(road.getRelativePosition((42, 1)), (42, 3))
        road = Road(100, 2, lane_width=10)
        self.assertEqual(road.getRelativePosition((0, 0)), (0, 5))
        self.assertEqual(road.getRelativePosition((42, 0)), (42, 5))
        self.assertEqual(road.getRelativePosition((0, 1)), (0, 15))
        self.assertEqual(road.getRelativePosition((42, 1)), (42, 15))

    def test_getAbsolutePosition(self):
        road = Road(100, 2, lane_width=1)
        for x in range(100):
            for lane in range(2):
                position = (x, lane)
                result = road.getAbsolutePosition(position=position)
                self.assertEqual(result, position, f'invalid position for ({x}, {lane})')
        road = Road(100, 2, lane_width=2)
        self.assertEqual(road.getAbsolutePosition((0, 1)), (0, 0))
        self.assertEqual(road.getAbsolutePosition((42, 1)), (42, 0))
        self.assertEqual(road.getAbsolutePosition((0, 3)), (0, 1))
        self.assertEqual(road.getAbsolutePosition((42, 3)), (42, 1))
        road = Road(100, 2, lane_width=10)
        self.assertEqual(road.getAbsolutePosition((0, 5)), (0, 0))
        self.assertEqual(road.getAbsolutePosition((42, 5)), (42, 0))
        self.assertEqual(road.getAbsolutePosition((0, 15)), (0, 1))
        self.assertEqual(road.getAbsolutePosition((42, 15)), (42, 1))

    def test_isProperPosition(self):
        road = Road(100, 1, lane_width=1)
        self.assertTrue(road.isProperPosition(position=(0, 0)))
        self.assertTrue(road.isProperPosition(position=(99, 0)))
        self.assertFalse(road.isProperPosition(position=(-1, 0)))
        self.assertFalse(road.isProperPosition(position=(100, 0)))
        self.assertFalse(road.isProperPosition(position=(0, 1)))
        self.assertFalse(road.isProperPosition(position=(0, -1)))
        road = Road(100, 1, lane_width=2)
        self.assertTrue(road.isProperPosition(position=(0, 1)))
        self.assertTrue(road.isProperPosition(position=(0, 2)))
        self.assertTrue(road.isProperPosition(position=(99, 1)))
        self.assertTrue(road.isProperPosition(position=(99, 2)))
        self.assertFalse(road.isProperPosition(position=(-1, 1)))
        self.assertFalse(road.isProperPosition(position=(100, 1)))
        self.assertFalse(road.isProperPosition(position=(0, 3)))

    def test_isSafePosition(self):
        road = Road(length=100, lanes_count=5, lane_width=1)
        proper = [True, True, True, False, False, False, False]
        vehicle = [None, Mock(), Mock(), None, None, Mock(), Mock()]
        pending = [Mock(), None, Mock(), None, Mock(), None, Mock()]
        for p, v, pv in zip(proper, vehicle, pending):
            road.isProperPosition = Mock(return_value=p)
            road.getVehicle = Mock(return_value=v)
            road.getPendingVehicle = Mock(return_value=pv)
            self.assertFalse(road.isSafePosition(position=(0, 0)))
        road.isProperPosition = Mock(return_value=True)
        road.getVehicle = Mock(return_value=None)
        road.getPendingVehicle = Mock(return_value=None)
        self.assertTrue(road.isSafePosition(position=(0, 0)))

    def test_canPlaceVehicle(self):
        road = Road(length=100, lanes_count=2, lane_width=2)
        vehicle = Mock(width=2, length=3, position=(2, 1))

        positions = [(0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
        calls = [call(position=position) for position in positions]

        def mock_isSafePosition(invalid: typing.Iterable[Position]) \
                -> typing.Callable[[Position], bool]:
            return lambda position: position not in invalid

        road.isSafePosition = Mock(side_effect=mock_isSafePosition([]))
        self.assertTrue(road.canPlaceVehicle(vehicle=vehicle))
        road.isSafePosition.assert_has_calls(calls, any_order=True)

        def powerset(xs):
            return chain.from_iterable(combinations(xs, r) for r in range(len(xs) + 1))

        for invalid in powerset(positions):
            if len(invalid) == 0:
                continue
            road.isSafePosition = Mock(side_effect=mock_isSafePosition(invalid=invalid))
            self.assertFalse(road.canPlaceVehicle(vehicle=vehicle), msg=f'invalid={invalid}')

    def test_step(self):
        road = Road(100, 1, lane_width=1)
        vehicle = Mock()
        road._updateLanes = lambda f: f(vehicle)
        road.step()
        vehicle.beforeMove.assert_called_once()
        vehicle.move.assert_called_once()


if __name__ == '__main__':
    unittest.main()
