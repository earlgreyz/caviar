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

    def __init__(self, length: int, lanes_count: int, lane_width: int,
                 controller: typing.Optional[SpeedController] = None):
        super().__init__(length, lanes_count, lane_width, controller=controller)
        self.lanes = [self._emptyLane() for _ in range(self.sublanesCount)]
        self.pending_lanes = [self._emptyLane() for _ in range(self.sublanesCount)]

    def _emptyLane(self) -> Lane:
        return [None] * self.length

    def addVehicle(self, vehicle: Vehicle) -> None:
        x, lane = vehicle.position
        for w in range(vehicle.width):
            for i in range(vehicle.length):
                if self.lanes[lane + w][x - i] is not None:
                    raise CollisionError()
        for w in range(vehicle.width):
            for i in range(vehicle.length):
                self.lanes[lane + w][x - i] = vehicle

    def getVehicle(self, position: Position) -> typing.Optional[Vehicle]:
        x, lane = position
        return self.lanes[lane][x]

    def getAllVehicles(self) -> typing.Generator[Vehicle, None, None]:
        for lane in range(self.sublanesCount):
            for x in reversed(range(self.length)):
                vehicle = self.lanes[lane][x]
                if vehicle is not None and vehicle.position == (x, lane):
                    yield vehicle

    def addPendingVehicle(self, vehicle: Vehicle) -> None:
        x, lane = vehicle.position
        for w in range(vehicle.width):
            for i in range(vehicle.length):
                if self.pending_lanes[lane + w][x - i] is not None:
                    raise CollisionError()
        for w in range(vehicle.width):
            for i in range(vehicle.length):
                self.pending_lanes[lane + w][x - i] = vehicle

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
        self.pending_lanes = [self._emptyLane() for _ in range(self.sublanesCount)]
