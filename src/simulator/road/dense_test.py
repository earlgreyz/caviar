import unittest

from simulator.road.dense import DenseRoad
from simulator.road.road_test import implementsRoad


@implementsRoad
class DenseRoadTestCase(unittest.TestCase):
    def getRoad(self, length: int, lanes: int) -> DenseRoad:
        return DenseRoad(length=length, lanes_count=lanes)


if __name__ == '__main__':
    unittest.main()
