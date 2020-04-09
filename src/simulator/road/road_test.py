import typing
import unittest
from unittest.mock import Mock

from simulator.road.road import Road, CollisionError
from simulator.statistics import AverageResult
from simulator.vehicle.vehicle import Vehicle, VehicleFlags


def implementsRoad(cls):
    assert hasattr(cls, 'getRoad') and callable(getattr(cls, 'getRoad'))

    def test_addVehicle(self: cls):
        # Add a vehicle.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=1)
        position = (0, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        # Try to add the vehicle outside the road length.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=1)
        position = (100, 0)
        vehicle.position = position
        with self.assertRaises(IndexError):
            road.addVehicle(vehicle)
        # Try to add the vehicle outside the road lanes.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=1)
        position = (0, 1)
        vehicle.position = position
        with self.assertRaises(IndexError):
            road.addVehicle(vehicle)
        # Try to add the vehicle to a nonempty road cell.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=1)
        position = (0, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        another: Vehicle = Mock(length=1)
        another.position = position
        with self.assertRaises(CollisionError):
            road.addVehicle(another)

    def test_getVehicle(self: cls):
        # Add and retrieve the vehicle.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=1)
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

    def test_addVehicle_long(self: cls):
        # Add and retrieve the vehicle.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=2)
        position = (1, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        result = road.getVehicle(position)
        self.assertEqual(result, vehicle)
        result = road.getVehicle((0, 0))
        self.assertEqual(result, vehicle)
        result = road.getVehicle((2, 0))
        self.assertIsNone(result)

    def test_allVehicles(self: cls):
        # Add and retrieve all the vehicles from a single lane.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicles: typing.List[Vehicle] = []
        for i in range(100):
            vehicle: Vehicle = Mock(length=1)
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
                vehicle: Vehicle = Mock(length=1)
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
        # Long vehicles should be returned at each occupied position.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicles: typing.List[Vehicle] = []
        for i in range(1, 100, 2):
            vehicle: Vehicle = Mock(length=2)
            vehicle.position = (i, 0)
            vehicles.extend([vehicle, vehicle])
            road.addVehicle(vehicle)
        result = list(road.getAllVehicles())
        self.assertEqual(len(result), len(vehicles), 'got invalid number of vehicles')
        self.assertListEqual(result, list(reversed(vehicles)), 'vehicle lists differ')

    def test_addPendingVehicle(self: cls):
        # Add a vehicle.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=1)
        position = (0, 0)
        vehicle.position = position
        road.addPendingVehicle(vehicle)
        # Try to add the vehicle outside the road length.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=1)
        position = (100, 0)
        vehicle.position = position
        with self.assertRaises(IndexError):
            road.addPendingVehicle(vehicle)
        # Try to add the vehicle outside the road lanes.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=1)
        position = (0, 1)
        vehicle.position = position
        with self.assertRaises(IndexError):
            road.addPendingVehicle(vehicle)
        # Try to add the vehicle to a nonempty road cell.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=1)
        position = (0, 0)
        vehicle.position = position
        road.addPendingVehicle(vehicle)
        another: Vehicle = Mock(length=1)
        another.position = position
        with self.assertRaises(CollisionError):
            road.addPendingVehicle(another)

    def test_getPendingVehicle(self: cls):
        # Add and retrieve the vehicle.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=1)
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

    def test_addPendingVehicle_long(self: cls):
        # Add and retrieve the vehicle.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=2)
        position = (1, 0)
        vehicle.position = position
        road.addPendingVehicle(vehicle)
        result = road.getPendingVehicle(position)
        self.assertEqual(result, vehicle)
        result = road.getPendingVehicle((0, 0))
        self.assertEqual(result, vehicle)
        result = road.getPendingVehicle((2, 0))
        self.assertIsNone(result)

    def test_getNextVehicle(self: cls):
        # Single lane.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock(length=1)
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
        vehicle: Vehicle = Mock(length=1)
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
        vehicle: Vehicle = Mock(length=1)
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
        vehicle: Vehicle = Mock(length=1)
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
            vehicle = Mock(length=1)
            vehicle.position = (x, 0)
            vehicles.append(vehicle)
            road.addPendingVehicle(vehicle)
        road._commitLanes()
        for x in range(100):
            result = road.getVehicle(position=(x, 0))
            self.assertEqual(result, vehicles[x], f'got invalid vehicle x={x}')

    def test_updateLanes(self: cls):
        road: Road = self.getRoad(length=10, lanes=1)
        vehicles: typing.List[Vehicle] = []
        for x in range(10):
            vehicle = Mock(length=1, flags=VehicleFlags.NONE)
            vehicle.isEmergency.return_value = False
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

    def test_updateLanes_long(self: cls):
        road: Road = self.getRoad(length=10, lanes=1)
        vehicles: typing.List[Vehicle] = []
        for i in range(1, 10, 2):
            vehicle: Vehicle = Mock(length=2, flags=VehicleFlags.NONE)
            vehicle.isEmergency.return_value = False
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

    cls.test_addVehicle = test_addVehicle
    cls.test_getVehicle = test_getVehicle
    cls.test_addVehicle_long = test_addVehicle_long
    cls.test_allVehicles = test_allVehicles
    cls.test_addPendingVehicle = test_addPendingVehicle
    cls.test_getPendingVehicle = test_getPendingVehicle
    cls.test_addPendingVehicle_long = test_addPendingVehicle_long
    cls.test_getNextVehicle = test_getNextVehicle
    cls.test_getPreviousVehicle = test_getPreviousVehicle
    cls.test_commitLanes = test_commitLanes
    cls.test_updateLanes = test_updateLanes
    cls.test_updateLanes_long = test_updateLanes_long
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

    def test_addEmergencyVehicle(self):
        road: Road = Road(length=100, lanes_count=1)
        vehicle = Mock(position=(0, 0))
        vehicle.isEmergency.return_value = False
        with self.assertRaises(ValueError):
            road.addEmergencyVehicle(vehicle)
        vehicle.isEmergency.return_value = True
        road.addVehicle = Mock()
        road.addEmergencyVehicle(vehicle)
        road.addVehicle.assert_called_once_with(vehicle=vehicle)
        self.assertCountEqual({vehicle}, road.emergency)

    def test_removeVehicle(self):
        road: Road = Road(length=100, lanes_count=1)
        vehicle = Mock(position=(0, 0))
        vehicle.isEmergency.return_value = False
        emergency = Mock(position=(1, 0))
        emergency.isEmergency.return_value = True
        road.emergency = {emergency}
        # Remove non-emergency vehicle.
        road._removeVehicle(vehicle)
        self.assertCountEqual({emergency}, road.emergency)
        self.assertCountEqual([vehicle], road.removed)
        # Remove emergency vehicle.
        road._removeVehicle(emergency)
        self.assertCountEqual({}, road.emergency)
        self.assertCountEqual([vehicle, emergency], road.removed)
        # Remove emergency vehicle not on the road.
        with self.assertRaises(KeyError):
            road._removeVehicle(emergency)

    def test_isProperPosition(self):
        road = Road(100, 1)
        self.assertTrue(road.isProperPosition(position=(0, 0)))
        self.assertTrue(road.isProperPosition(position=(99, 0)))
        self.assertFalse(road.isProperPosition(position=(-1, 0)))
        self.assertFalse(road.isProperPosition(position=(100, 0)))
        self.assertFalse(road.isProperPosition(position=(0, 1)))
        self.assertFalse(road.isProperPosition(position=(0, -1)))

    def test_isSafePosition(self):
        road = Road(length=100, lanes_count=5)
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

    def test_getAverageVelocityFiltered(self):
        road = Road(100, 1)
        vehicles: typing.List[Vehicle] = []
        for velocity in range(10):
            vehicle = Mock()
            vehicle.velocity = velocity
            vehicles.append(vehicle)
        road.getAllVehicles = lambda: vehicles
        # No vehicles matching the predicate.
        result = road.getAverageVelocityFiltered(lambda _: False)
        expected = AverageResult(value=0, count=0)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))
        # All vehicles matching the predicate.
        result = road.getAverageVelocityFiltered(lambda _: True)
        expected = AverageResult(value=45, count=10)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

        # Some vehicles matching the predicate.
        def isEven(vehicle):
            return vehicle.velocity % 2 == 0

        result = road.getAverageVelocityFiltered(isEven)
        expected = AverageResult(value=20, count=5)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

    def test_getAverageVelocity(self):
        road = Road(100, 1)
        vehicles: typing.List[Vehicle] = []
        for velocity in range(10):
            vehicle = Mock()
            vehicle.velocity = velocity
            vehicles.append(vehicle)
        road.getAllVehicles = lambda: vehicles
        result = road.getAverageVelocity()
        expected = AverageResult(value=45, count=10)
        self.assertEqual(result, expected, '{} != {}'.format(str(result), str(expected)))

    def test_step(self):
        road = Road(100, 1)
        vehicle = Mock()
        road._updateLanes = lambda f: f(vehicle)
        road.step()
        vehicle.beforeMove.assert_called_once()
        vehicle.move.assert_called_once()


if __name__ == '__main__':
    unittest.main()
