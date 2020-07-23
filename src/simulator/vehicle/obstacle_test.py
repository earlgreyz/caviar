import unittest

from simulator.position import Position
from simulator.vehicle.obstacle import Obstacle
from simulator.vehicle.vehicle_test import implementsVehicle


@implementsVehicle
class ObstacleTestCase(unittest.TestCase):
    def getVehicle(self, position: Position) -> Obstacle:
        return Obstacle(position=position, width=1, length=1)

    def test_beforeMove(self):
        position = (42, 2)
        obstacle = Obstacle(position=position, width=2, length=10)
        after = obstacle.beforeMove()
        self.assertEqual(position, after)
        self.assertEqual(position, obstacle.position)
        self.assertEqual(2, obstacle.width)
        self.assertEqual(10, obstacle.length)

    def test_move(self):
        position = (42, 2)
        obstacle = Obstacle(position=position, width=2, length=10)
        after = obstacle.move()
        self.assertEqual(position, after)
        self.assertEqual(position, obstacle.position)
        self.assertEqual(2, obstacle.width)
        self.assertEqual(10, obstacle.length)


if __name__ == '__main__':
    unittest.main()
