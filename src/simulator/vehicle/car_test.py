import unittest
from unittest.mock import Mock, patch

from simulator.position import Position
from simulator.vehicle.car import Car, isConventional, CarParams
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

    def test_shouldChangeLane(self):
        road = Mock()
        position = (10, 0)
        destination = (10, 1)
        limit = 5
        car = Car(position=position, velocity=limit + 1, road=road)

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
        # A vehicle is approaching from behind.
        road.getNextVehicle.return_value = (100, None)
        road.controller.getMaxSpeed.return_value = 5
        road.getPreviousVehicle.return_value = (5, Mock())
        self.assertFalse(car._shouldChangeLane(destination))
        # Lane change is possible.
        road.getPreviousVehicle.return_value = (0, Mock())
        self.assertTrue(car._shouldChangeLane(destination))
        road.getPreviousVehicle.return_value = (-1, None)
        self.assertTrue(car._shouldChangeLane(destination))

    @patch('random.random')
    def test_changeLane(self, patched_random):
        road = Mock()
        car = Car(position=(0, 0), velocity=5, road=road)
        # Unable to change the lane.
        ccls = [False, False, True]
        scls = [False, True, False]
        for ccl, scl in zip(ccls, scls):
            car._canChangeLane = Mock(return_value=ccl)
            car._shouldChangeLane = Mock(return_value=scl)
            self.assertFalse(car._changeLane(destination=(0, 1)))
        # Can change the lane.
        car._canChangeLane = Mock(return_value=True)
        car._shouldChangeLane = Mock(return_value=True)
        # Change probability 0.5
        car.params.lane_change_probability = 0.5
        patched_random.return_value = 0.
        self.assertTrue(car._changeLane(destination=(0, 1)))
        patched_random.return_value = 0.49
        self.assertTrue(car._changeLane(destination=(0, 1)))
        patched_random.return_value = 0.5
        self.assertFalse(car._changeLane(destination=(0, 1)))
        patched_random.return_value = 0.99
        self.assertFalse(car._changeLane(destination=(0, 1)))
        # Change probability 0
        car.params.lane_change_probability = 0.
        patched_random.return_value = 0.
        self.assertFalse(car._changeLane(destination=(0, 1)))
        patched_random.return_value = 0.99
        self.assertFalse(car._changeLane(destination=(0, 1)))
        # Change probability 1
        car.params.lane_change_probability = 1.
        patched_random.return_value = 0.
        self.assertTrue(car._changeLane(destination=(0, 1)))
        patched_random.return_value = 0.99
        self.assertTrue(car._changeLane(destination=(0, 1)))

    @patch('simulator.vehicle.car.shuffled')
    def test_beforeMove(self, mocked_shuffled):
        mocked_shuffled.side_effect = lambda xs: xs
        road = Mock()
        # Lanes not changed.
        car = Car(position=(42, 1), velocity=5, road=road)
        car._changeLane = Mock(return_value=False)
        position = car.beforeMove()
        self.assertEqual(position, (42, 1))
        self.assertEqual(car.position, (42, 1))
        # Change to the first available lane.
        car = Car(position=(42, 1), velocity=5, road=road)
        car._changeLane = Mock(return_value=True)
        position = car.beforeMove()
        self.assertEqual(position, (42, 0))
        self.assertEqual(car.position, (42, 0))
        # Change to the second available lane.
        car = Car(position=(42, 1), velocity=5, road=road)
        car._changeLane = Mock(side_effect=[False, True])
        position = car.beforeMove()
        self.assertEqual(position, (42, 2))
        self.assertEqual(car.position, (42, 2))

    @patch('random.random')
    def test_move(self, patched_random):
        # No slowdown.
        car = Car(position=(0, 0), velocity=5, road=Mock(), params=CarParams(slow=0))
        patched_random.return_value = 1
        car._getMaxSpeed = Mock(return_value=5)
        position = car.move()
        self.assertEqual(position, (5, 0))
        # Speed up.
        car = Car(position=(0, 0), velocity=3, road=Mock(), params=CarParams(slow=0))
        patched_random.return_value = 1
        car._getMaxSpeed = Mock(return_value=5)
        position = car.move()
        self.assertEqual(position, (4, 0))
        # Slowdown.
        car = Car(position=(0, 0), velocity=3, road=Mock(), params=CarParams(slow=1))
        patched_random.return_value = 0
        car._getMaxSpeed = Mock(return_value=5)
        position = car.move()
        self.assertEqual(position, (2, 0))

    def test_isConventional(self):
        car = self.getVehicle(position=(0, 0))
        self.assertTrue(isConventional(car))
        vehicle = Vehicle(position=(0, 0), velocity=0)
        self.assertFalse(isConventional(vehicle))


if __name__ == '__main__':
    unittest.main()
