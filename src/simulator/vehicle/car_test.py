import unittest
from unittest.mock import Mock

from simulator.position import Position
from simulator.vehicle.car import Car
from simulator.vehicle.vehicle import Vehicle
from simulator.vehicle.vehicle_test import implementsVehicle


@implementsVehicle
class CarTestCase(unittest.TestCase):
    def getVehicle(self, position: Position) -> Vehicle:
        road = Mock()
        road.isProperPosition.return_value = False
        road.getNextVehicle.return_value = (100, None)
        road.getPreviousVehicle.return_value = (-1, None)
        road.controller = Mock()
        road.controller.getMaxSpeed.return_value = 5
        return Car(position=position, velocity=1, road=road)

    def test_getMaxSpeed(self):
        road = Mock()
        road.controller = Mock()
        road.controller.getMaxSpeed.return_value = 5
        car = Car(position=(0, 0), velocity=5, road=road)
        # No vehicles in front.
        road.getNextVehicle.return_value = (100, None)
        limit = car._getMaxSpeed(position=(0, 0))
        self.assertEqual(limit, 5, 'expected road limit=5')
        # Vehicle in front is far away.
        road.getNextVehicle.return_value = (10, Mock())
        limit = car._getMaxSpeed(position=(0, 0))
        self.assertEqual(limit, 5, 'expected road limit=5')
        # Vehicle in front is blocking the road.
        road.getNextVehicle.return_value = (2, Mock())
        limit = car._getMaxSpeed(position=(0, 0))
        self.assertEqual(limit, 1, 'expected min distance=1')

    def test_canChangeLane(self):
        road = Mock()
        car = Car(position=(0, 0), velocity=5, road=road)
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


if __name__ == '__main__':
    unittest.main()
