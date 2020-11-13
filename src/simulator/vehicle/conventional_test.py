import unittest
from unittest.mock import Mock, patch

from simulator.position import Position
from simulator.vehicle.conventional import ConventionalCar, Driver, isConventional
from simulator.vehicle.obstacle import Obstacle
from simulator.vehicle.vehicle import Vehicle
from simulator.vehicle.vehicle_test import implementsVehicle


@implementsVehicle
class ConventionalCarTestCase(unittest.TestCase):
    def getVehicle(self, position: Position) -> Vehicle:
        road = Mock(length=100, lane_width=1)
        road.isProperPosition.return_value = False
        road.getNextVehicle.return_value = (100, None)
        road.getPreviousVehicle.return_value = (-1, None)
        road.controller = Mock()
        road.controller.getMaxSpeed.return_value = 5
        return ConventionalCar(position=position, velocity=1, road=road)

    @patch('simulator.vehicle.conventional.shuffled')
    def test_tryChangeLanes(self, mocked_shuffled):
        mocked_shuffled.side_effect = lambda xs: xs
        road = Mock(lane_width=1)
        # Lanes not changed.
        car = ConventionalCar(position=(42, 1), velocity=5, road=road)
        car._canChangeLane = Mock(return_value=False)
        self.assertFalse(car._tryChangeLanes())
        self.assertEqual(car.position, (42, 1))
        # Change to the first available lane.
        car = ConventionalCar(position=(42, 1), velocity=5, road=road)
        car._canChangeLane = Mock(return_value=True)
        self.assertTrue(car._tryChangeLanes())
        self.assertEqual(car.position, (42, 0))
        # Change to the second available lane.
        car = ConventionalCar(position=(42, 1), velocity=5, road=road)
        car._canChangeLane = Mock(side_effect=[False, True])
        self.assertTrue(car._tryChangeLanes())
        self.assertEqual(car.position, (42, 2))

    @patch('simulator.vehicle.conventional.shuffled')
    def test_tryAvoidObstacle(self, mocked_shuffled):
        mocked_shuffled.side_effect = lambda xs: xs
        # No obstacles on the road.
        road = Mock(lane_width=1)
        road.getNextVehicle.return_value = -1, None
        car = ConventionalCar(position=(42, 1), velocity=5, road=road)
        self.assertFalse(car._tryAvoidObstacle())
        # Not an obstacle on the road in front.
        road = Mock(lane_width=1)
        road.getNextVehicle.return_value = 44, Mock()
        car = ConventionalCar(position=(42, 1), velocity=5, road=road)
        self.assertFalse(car._tryAvoidObstacle())
        # Obstacle is far away.
        road = Mock(lane_width=1)
        road.getNextVehicle.return_value = 120, Obstacle(position=(120, 2), length=1, width=1)
        car = ConventionalCar(position=(42, 1), velocity=5, road=road)
        self.assertFalse(car._tryAvoidObstacle())
        # Lanes not changed.
        road = Mock(lane_width=1)
        road.getNextVehicle.return_value = 44, Obstacle(position=(44, 2), length=1, width=1)
        car = ConventionalCar(position=(42, 1), velocity=5, road=road)
        car._canAvoid = Mock(return_value=False)
        car._avoid = Mock()
        self.assertFalse(car._tryAvoidObstacle())
        car._avoid.assert_not_called()
        self.assertEqual(car.position, (42, 1))
        # Change to the first available lane.
        road = Mock(lane_width=1)
        road.getNextVehicle.return_value = 44, Obstacle(position=(44, 2), length=1, width=1)
        car = ConventionalCar(position=(42, 1), velocity=5, road=road)
        car._canAvoid = Mock(return_value=True)
        car._avoid = Mock()
        self.assertTrue(car._tryAvoidObstacle())
        car._avoid.assert_called_once()
        self.assertEqual(car.position, (42, 0))
        # Change to the second available lane.
        road = Mock(lane_width=1)
        road.getNextVehicle.return_value = 44, Obstacle(position=(44, 2), length=1, width=1)
        car = ConventionalCar(position=(42, 1), velocity=5, road=road)
        car._avoid = Mock()
        car._canAvoid = Mock(side_effect=[False, True])
        self.assertTrue(car._tryAvoidObstacle())
        car._avoid.assert_called_once()
        self.assertEqual(car.position, (42, 2))

    @patch('random.random')
    def test_move(self, patched_random):
        # No slowdown.
        car = ConventionalCar(position=(0, 0), velocity=5, road=Mock(), driver=Driver(slow=0))
        patched_random.return_value = 1
        car._getMaxSpeed = Mock(return_value=5)
        position = car.move()
        self.assertEqual(position, (5, 0))
        # Speed up.
        car = ConventionalCar(position=(0, 0), velocity=3, road=Mock(), driver=Driver(slow=0))
        patched_random.return_value = 1
        car._getMaxSpeed = Mock(return_value=5)
        position = car.move()
        self.assertEqual(position, (4, 0))
        # Slowdown.
        car = ConventionalCar(position=(0, 0), velocity=3, road=Mock(), driver=Driver(slow=1))
        patched_random.return_value = 0
        car._getMaxSpeed = Mock(return_value=5)
        position = car.move()
        self.assertEqual(position, (2, 0))

    @patch('random.random')
    @patch('simulator.vehicle.conventional.Car._canChangeLane')
    def test_canChangeLane(self, patched_change, patched_random):
        road = Mock()
        car = ConventionalCar(position=(0, 0), velocity=5, road=road)
        patched_change.return_value = True
        # Change probability 0.5
        car.driver.change = 0.5
        patched_random.return_value = 0.
        self.assertTrue(car._canChangeLane(destination=(0, 1)))
        patched_random.return_value = 0.49
        self.assertTrue(car._canChangeLane(destination=(0, 1)))
        patched_random.return_value = 0.5
        self.assertFalse(car._canChangeLane(destination=(0, 1)))
        patched_random.return_value = 0.99
        self.assertFalse(car._canChangeLane(destination=(0, 1)))
        # Change probability 0
        car.driver.change = 0.
        patched_random.return_value = 0.
        self.assertFalse(car._canChangeLane(destination=(0, 1)))
        patched_random.return_value = 0.99
        self.assertFalse(car._canChangeLane(destination=(0, 1)))
        # Change probability 1
        car.driver.change = 1.
        patched_random.return_value = 0.
        self.assertTrue(car._canChangeLane(destination=(0, 1)))
        patched_random.return_value = 0.99
        self.assertTrue(car._canChangeLane(destination=(0, 1)))

    def test_isConventional(self):
        car = self.getVehicle(position=(0, 0))
        self.assertTrue(isConventional(car))
        vehicle = Vehicle(position=(0, 0), velocity=0)
        self.assertFalse(isConventional(vehicle))


if __name__ == '__main__':
    unittest.main()
