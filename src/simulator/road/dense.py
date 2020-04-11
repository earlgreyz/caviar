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

    def addVehicle(self, vehicle: Vehicle) -> None:
        x, lane = vehicle.position
        for i in range(vehicle.length):
            if self.lanes[lane][x - i] is not None:
                raise CollisionError()
        for i in range(vehicle.length):
            self.lanes[lane][x - i] = vehicle

    def getVehicle(self, position: Position) -> typing.Optional[Vehicle]:
        x, lane = position
        return self.lanes[lane][x]

    def getAllVehicles(self) -> typing.Generator[Vehicle, None, None]:
        for x in reversed(range(self.length)):
            for lane in range(self.lanes_count):
                if self.lanes[lane][x] is not None:
                    yield self.lanes[lane][x]

    def addPendingVehicle(self, vehicle: Vehicle) -> None:
        x, lane = vehicle.position
        for i in range(vehicle.length):
            if self.pending_lanes[lane][x - i] is not None:
                raise CollisionError()

        for i in range(vehicle.length):
            self.pending_lanes[lane][x - i] = vehicle
        self.pending_lanes[lane][x] = vehicle

    def getPendingVehicle(self, position: Position) -> typing.Optional[Vehicle]:
        x, lane = position
        return self.pending_lanes[lane][x]

    def getNextVehicle(self, position: Position) -> typing.Tuple[int, typing.Optional[Vehicle]]:
        x, lane = position
        if not self.isProperPosition(position):
            raise IndexError(f'position {position} not on the road')
        for i in range(x + 1, self.length):
            if self.lanes[lane][i] is not None:
                return i, self.lanes[lane][i]
        return self.length, None

    def getPreviousVehicle(self, position: Position) -> typing.Tuple[int, typing.Optional[Vehicle]]:
        x, lane = position
        if not self.isProperPosition(position):
            raise IndexError(f'position {position} not on the road')
        for i in range(x - 1, -1, -1):
            if self.lanes[lane][i] is not None:
                return i, self.lanes[lane][i]
        return -1, None

    def _commitLanes(self) -> None:
        self.lanes = self.pending_lanes
        self.pending_lanes = [self._emptyLane() for _ in range(self.lanes_count)]
