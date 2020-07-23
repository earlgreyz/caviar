import click
import typing

from simulator.position import inBounds
from simulator.road.road import Road
from simulator.vehicle.obstacle import Obstacle

ObstacleValue = typing.Tuple[int, int, int]


class ObstacleParamType(click.ParamType):
    name = 'obstacle'

    def convert(self, value: str, param: click.Parameter, ctx: click.Context) -> ObstacleValue:
        tmp = value.split(':')
        if len(tmp) != 2:
            self._invalidFormat(value, param, ctx)
        lane, tmp = tmp
        tmp = tmp.split('-')
        if len(tmp) != 2:
            self._invalidFormat(value, param, ctx)
        begin, end = tmp
        try:
            return int(lane), int(begin), int(end)
        except ValueError:
            self.fail(
                f'expected valid integers, got LANE="{lane}", BEGIN="{begin}", END="{end}"',
                param,
                ctx,
            )

    def _invalidFormat(self, value: str, param: click.Parameter, ctx: click.Context) -> None:
        self.fail(
            f'expected obstacle to be of format LANE:BEGIN-END, got "{value}" instead',
            param,
            ctx,
        )


def addObstacle(road: Road, obstacle: ObstacleValue) -> None:
    lane, begin, end = obstacle
    if not inBounds(lane, 0, road.lanes_count):
        raise ValueError(f'invalid obstacle, lane {lane} is not on the road')
    if not inBounds(begin, 0, road.length) or not inBounds(end, 0, road.length):
        raise ValueError(f'invalid obstacle, position {(begin, end)} is not on the road')

    length = end - begin + 1
    width = road.lane_width
    position = road.getRelativePosition(position=(end, lane))
    obstacle = Obstacle(position=position, width=width, length=length)
    road.addVehicle(obstacle)
