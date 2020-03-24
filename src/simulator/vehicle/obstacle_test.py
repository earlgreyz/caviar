import unittest

from simulator.position import Position
from simulator.vehicle.obstacle import Obstacle
from simulator.vehicle.vehicle_test import implementsVehicle


@implementsVehicle
class ObstacleTestCase(unittest.TestCase):
    def getVehicle(self, position: Position) -> Obstacle:
        return Obstacle(position=position)

    def test_init(self):
        position = (42, 2)
        obstacle = Obstacle(position=position)
        self.assertEqual(obstacle.position, position, 'positions differ')

    def test_beforeMove(self):
        before = (42, 2)
        obstacle = Obstacle(position=before)
        after = obstacle.beforeMove()
        self.assertEqual(before, after, 'positions differ')

    def test_move(self):
        before = (42, 2)
        obstacle = Obstacle(position=before)
        after = obstacle.move()
        self.assertEqual(before, after, 'positions differ')


if __name__ == '__main__':
    unittest.main()
