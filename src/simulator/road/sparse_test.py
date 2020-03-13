import unittest

from simulator.road.road_test import implementsRoad
from simulator.road.sparse import SparseRoad


@implementsRoad
class SparseRoadTestCase(unittest.TestCase):
    def getRoad(self, length: int, lanes: int) -> SparseRoad:
        return SparseRoad(length=length, lanes_count=lanes)


if __name__ == '__main__':
    unittest.main()
