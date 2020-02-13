import typing

from sortedcontainers import SortedDict

from simulator.position import Position
from simulator.road.road import Road, RoadParams
from simulator.vehicle.vehicle import Vehicle

Lane = SortedDict  # SortedDict[int, typing.Optional[Vehicle]]


class SparseRoad(Road):
    '''
    Road implementation for non traffic heavy roads.
    '''
    lanes: typing.List[Lane]
    pending_lanes: typing.List[Lane]

    def __init__(self, length: int, lanes_count: int, params: typing.Optional[RoadParams] = None):
        super().__init__(length=length, lanes_count=lanes_count, params=params)
        # Initialize lanes.
        self.lanes = [Lane() for _ in range(self.lanes_count)]
        self.pending_lanes = [Lane() for _ in range(self.lanes_count)]

    def addVehicle(self, position: Position, vehicle: Vehicle) -> None:
        x, lane = position
        self.lanes[lane][x] = vehicle

    def getVehicle(self, position: Position) -> typing.Optional[Vehicle]:
        x, lane = position
        if x in self.lanes[lane]:
            return self.lanes[lane][x]
        return None

    def getAllVehicles(self) -> typing.Generator[Vehicle, None, None]:
        for lane in self.lanes:
            for vehicle in lane.values():
                yield vehicle

    def addPendingVehicle(self, position: Position, vehicle: Vehicle) -> None:
        x, lane = position
        self.pending_lanes[lane][x] = vehicle

    def getMaxSpeed(self, position: Position) -> int:
        next, vehicle = self.getNextVehicle(position=position)
        if vehicle is None:
            return self.params.MAX_SPEED
        else:
            return min(self.params.MAX_SPEED, next - position[0])

    def getNextVehicle(self, position: Position) -> typing.Tuple[int, typing.Optional[Vehicle]]:
        x, lane = position
        next = self.lanes[lane].bisect_right(x)
        if next == len(self.lanes[lane]):
            return (self.length, None)
        else:
            return self.lanes[lane].peekitem(next)

    def _commitLanes(self) -> None:
        self.lanes = self.pending_lanes
        self.pending_lanes = [Lane() for _ in range(self.lanes_count)]
