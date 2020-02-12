import typing

from sortedcontainers import SortedDict

from simulator.position import Position
from simulator.vehicle.vehicle import Vehicle

Lane = SortedDict  # SortedDict[int, typing.Optional[Vehicle]]


class RoadParams:
    MAX_SPEED: int

    def __init__(self, speed: int = 5):
        self.MAX_SPEED = speed


class Road:
    params: RoadParams

    length: int
    lanes_count: int
    lanes: typing.List[Lane]
    pending_lanes: typing.List[Lane]

    vehicles_count: int

    def __init__(self, length: int, lanes_count: int, params: typing.Optional[RoadParams] = None):
        self.length = length
        self.lanes_count = lanes_count
        self.lanes = [SortedDict() for _ in range(lanes_count)]
        self.pending_lanes = [SortedDict() for _ in range(lanes_count)]
        self.vehicles_count = 0
        self.params = params if params is not None else RoadParams()

    def __updateLanes(self, f: typing.Callable[[Vehicle], Position]) -> None:
        for lane in self.lanes:
            for vehicle in lane.values():
                x, i = f(vehicle)
                if x < self.length:
                    self.pending_lanes[i][x] = vehicle
                else:
                    self.vehicles_count -= 1
        self.lanes = self.pending_lanes
        self.pending_lanes = [SortedDict() for _ in range(self.lanes_count)]

    def step(self) -> None:
        self.__updateLanes(lambda vehicle: vehicle.beforeMove())
        self.__updateLanes(lambda vehicle: vehicle.move())

    def canChangeLane(self, position: Position) -> bool:
        x, lane = position
        if lane < 0 or lane >= self.lanes_count:
            return False
        return x not in self.lanes[lane]

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

    def addVehicle(self, position: Position, vehicle: Vehicle) -> None:
        x, lane = position
        self.lanes[lane][x] = vehicle
        self.vehicles_count += 1
