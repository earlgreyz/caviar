import typing

from simulator.position import Position
from simulator.vehicle.vehicle import Vehicle


class RoadParams:
    MAX_SPEED: int

    def __init__(self, speed: int = 5):
        self.MAX_SPEED = speed


class Road:
    params: RoadParams

    # Road options.
    length: int
    lanes_count: int

    # Statistics.
    vehicles_count: int

    def __init__(self, length: int, lanes_count: int, params: typing.Optional[RoadParams] = None):
        self.params = params if params is not None else RoadParams()
        self.length = length
        self.lanes_count = lanes_count
        # Initialize statistics.
        self.vehicles_count = 0

    def addVehicle(self, position: Position, vehicle: Vehicle) -> None:
        '''
        Adds a new vehicle to the road.
        :param position: position on the road.
        :param vehicle: vehicle to add.
        :return: None.
        '''
        raise NotImplementedError()

    def getVehicle(self, position: Position) -> typing.Optional[Vehicle]:
        '''
        Gets a vehicle from the road.
        :param position: position on the road.
        :return: a vehicle currently at the given position or None.
        '''
        raise NotImplementedError()

    def getAllVehicles(self) -> typing.Generator[Vehicle, None, None]:
        '''
        Gets all the vehicles on the road.
        :return: generator yielding all the vehicles.
        '''
        raise NotImplementedError()

    def addPendingVehicle(self, position: Position, vehicle: Vehicle) -> None:
        '''
        Adds the vehicle to the road which will be added on the next commit.
        :param position: position on the road.
        :param vehicle: vehicle to add.
        :return: None.
        '''
        raise NotImplementedError

    def getMaxSpeed(self, position: Position) -> int:
        '''
        Gets maximum speed at the given position of the road.
        :param position: position on the road.
        :return: maximum allowed speed.
        '''
        raise NotImplementedError()

    def getNextVehicle(self, position: Position) -> typing.Tuple[int, typing.Optional[Vehicle]]:
        '''
        Gets the vehicle in front of a given position.
        :param position: position on the road.
        :return: position and the vehicle or None.
        '''
        raise NotImplementedError()

    def isProperPosition(self, position: Position) -> bool:
        '''
        Checks if a position is a proper position on the road.
        :param position: position on the road.
        :return: if a position is on the road.
        '''
        x, lane = position
        return lane >= 0 and lane < self.lanes_count and x >= 0 and x < self.length

    def _commitLanes(self) -> None:
        '''
        Moves the pending vehicles to the actual road and clears the pending road.
        :return: None.
        '''
        raise NotImplementedError()

    def _updateLanes(self, f: typing.Callable[[Vehicle], Position]) -> None:
        '''
        Performs an update function on each of the vehicles on the road. Actions are
        performed at the same time on each of the vehicles and the road gets committed.
        :param f: update function.
        :return: None.
        '''
        for vehicle in self.getAllVehicles():
            x, i = f(vehicle)
            if x < self.length:
                self.addPendingVehicle(position=(x, i), vehicle=vehicle)
            else:
                self.vehicles_count -= 1
        self._commitLanes()

    def step(self) -> None:
        '''
        Performs a single simulation step moving all the vehicles.
        :return: None.
        '''
        self._updateLanes(lambda vehicle: vehicle.beforeMove())
        self._updateLanes(lambda vehicle: vehicle.move())

    # Statistics
    def getAverageVelocity(self) -> float:
        if self.vehicles_count == 0:
            return 0.
        velocity = 0
        for vehicle in self.getAllVehicles():
            velocity += vehicle.velocity
        return float(velocity) / self.vehicles_count
