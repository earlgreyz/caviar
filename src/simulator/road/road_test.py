import unittest
from unittest.mock import Mock

from simulator.road.road import Road, CollisionError
from simulator.vehicle.vehicle import Vehicle


def implementsRoad(cls):
    assert hasattr(cls, 'getRoad') and callable(getattr(cls, 'getRoad'))

    def test_addVehicle(self: cls):
        # Add and retrieve the vehicle.
        road: Road = self.getRoad(length=100, lanes=1)
        vehicle: Vehicle = Mock()
        position = (0, 0)
        vehicle.position = position
        road.addVehicle(vehicle)
        result = road.getVehicle(position)
        self.assertEqual(result, vehicle, 'added invalid vehicle')
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
        self.assertIsNone(result, 'got unexpected  vehicle')
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

    cls.test_addVehicle = test_addVehicle
    cls.test_getVehicle = test_getVehicle
    return cls


class RoadTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
