import typing

from simulator.position import Position
from simulator.road.road import Road, CollisionError
from simulator.road.speedcontroller import SpeedController
from simulator.vehicle.vehicle import Vehicle

Lane = typing.List[typing.Optional[Vehicle]]


class DenseRoad(Road):
    '''
    Road implementation for traffic heavy roads.
    '''
    lanes: typing.List[Lane]
    pending_lanes: typing.List[Lane]

    def __init__(self, length: int, lanes_count: int,
                 controller: typing.Optional[SpeedController] = None):
        super().__init__(length=length, lanes_count=lanes_count, controller=controller)
        # Initialize lanes.
        self.lanes = [self._emptyLane() for _ in range(self.lanes_count)]
        self.pending_lanes = [self._emptyLane() for _ in range(self.lanes_count)]

    def _emptyLane(self) -> Lane:
        return [None] * self.length

    def addVehicle(self,  vehicle: Vehicle) -> None:
        x, lane = vehicle.position
        if x in self.lanes[lane]:
            raise CollisionError()
        self.lanes[lane][x] = vehicle

    def getVehicle(self, position: Position) -> typing.Optional[Vehicle]:
        x, lane = position
        return self.lanes[lane][x]

    def getAllVehicles(self) -> typing.Generator[Vehicle, None, None]:
        for lane in self.lanes:
            for vehicle in reversed(lane):
                if vehicle is not None:
                    yield vehicle

    def addPendingVehicle(self, vehicle: Vehicle) -> None:
        x, lane = vehicle.position
        if x in self.lanes[lane]:
            raise CollisionError()
        self.pending_lanes[lane][x] = vehicle

    def getNextVehicle(self, position: Position) -> typing.Tuple[int, typing.Optional[Vehicle]]:
        x, lane = position
        for i in range(x + 1, self.length):
            if self.lanes[lane][i] is not None:
                return i, self.lanes[lane][i]
        return self.length, None

    def _commitLanes(self) -> None:
        self.lanes = self.pending_lanes
        self.pending_lanes = [self._emptyLane() for _ in range(self.lanes_count)]
