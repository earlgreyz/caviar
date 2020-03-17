import typing
from collections import defaultdict

from intervaltree import IntervalTree, Interval

from simulator.position import Position


class SpeedController:
    max_speed: int
    limits: typing.Dict[int, IntervalTree]

    def __init__(self, max_speed: int = 5):
        self.max_speed = max_speed
        self.limits = defaultdict(IntervalTree)

    def addLimit(self, lane: int, begin: int, end: int, limit: int) -> None:
        '''
        Adds new limit to the speed controller.
        :param lane: lane affected by the speed limit.
        :param begin: speed limit start position.
        :param end: speed limit end position.
        :param limit: limit value.
        :return: None.
        '''
        self.limits[lane].addi(begin=begin, end=end + 1, data=limit)

    def getMaxSpeed(self, position: Position) -> int:
        '''
        Returns maximum speed at the given position.
        :param position: position on the road.
        :return: maximum speed.
        '''
        x, lane = position
        if lane not in self.limits:
            return self.max_speed
        limits: typing.Set[Interval] = self.limits[lane].at(x)
        if len(limits) == 0:
            return self.max_speed
        return min((limit.data for limit in limits))
