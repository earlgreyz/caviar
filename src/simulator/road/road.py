import typing

from simulator.position import Position, inBounds
from simulator.road.speedcontroller import SpeedController
from simulator.vehicle.vehicle import Vehicle, VehicleFlags


class Road:
    controller: SpeedController

    # Road options.
    length: int
    lanes_count: int
    lane_width: int

    removed: typing.List[Vehicle]

    def __init__(self, length: int, lanes_count: int, lane_width: int,
                 controller: typing.Optional[SpeedController] = None):
        self.length = length
        self.lanes_count = lanes_count
        self.lane_width = lane_width
        self.controller = controller if controller is not None else SpeedController()
        self.removed = []

    @property
    def sublanesCount(self) -> int:
        '''
        Returns the actual sub-lanes count.
        :return: number of sub-lanes.
        '''
        return self.lanes_count * self.lane_width + self.lane_width // 2 * 2

    def getRelativePosition(self, position: Position) -> Position:
        '''
        Translates absolute position (not considering the lanes division) to the relative position
        on the road.
        :param position: absolute position.
        :return: relative position.
        '''
        x, lane = position
        return x, lane * self.lane_width + self.lane_width // 2

    def getAbsolutePosition(self, position: Position) -> Position:
        '''
        Translates relative position (considering the lanes division) to the absolute position
        on the road.
        :param position:
        :return:
        '''
        x, lane = position
        return x, (lane - self.lane_width // 2) // self.lane_width

    def addVehicle(self, vehicle: Vehicle) -> None:
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

    def addPendingVehicle(self, vehicle: Vehicle) -> None:
        '''
        Adds the vehicle to the road which will be added on the next commit.
        :param position: position on the road.
        :param vehicle: vehicle to add.
        :return: None.
        '''
        raise NotImplementedError

    def getPendingVehicle(self, position: Position) -> typing.Optional[Vehicle]:
        '''
        Gets a vehicle from the road which will be added on the next commit.
        :param position: position on the road.
        :return: a vehicle currently at the given pending position or None.
        '''
        raise NotImplementedError()

    def getNextVehicle(self, position: Position) -> typing.Tuple[int, typing.Optional[Vehicle]]:
        '''
        Gets the vehicle in front of a given position.
        :param position: position on the road.
        :return: position and the vehicle or None.
        '''
        raise NotImplementedError()

    def getPreviousVehicle(self, position: Position) -> typing.Tuple[int, typing.Optional[Vehicle]]:
        '''
        Gets the vehicle in in the back of a given position.
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
        return \
            inBounds(lane, self.lane_width // 2, self.sublanesCount - self.lane_width // 2) \
            and inBounds(x, 0, self.length)

    def isSafePosition(self, position: Position) -> bool:
        '''
        Checks if a position is safe to place a vehicle in.
        :param position: position on the road.
        :return: if a position is safe.
        '''
        return \
            self.isProperPosition(position=position) and \
            self.getVehicle(position=position) is None and \
            self.getPendingVehicle(position=position) is None

    def canPlaceVehicle(self, vehicle: Vehicle) -> bool:
        '''
        Checks if a given vehicle can be placed on the road.
        :param vehicle: vehicle to check.
        :return: if a vehicle can be placed.
        '''
        x, lane = vehicle.position
        return \
            all(self.isSafePosition(position=(x - i, lane + j))
                for i in range(vehicle.length) for j in range(vehicle.width))

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
        # Reset MOVED flag to keep track of vehicles already moved.
        for vehicle in self.getAllVehicles():
            vehicle.flags &= ~VehicleFlags.MOVED

        for vehicle in self.getAllVehicles():
            # Skip vehicles with MOVED flag set.
            if VehicleFlags.MOVED in vehicle.flags:
                continue
            vehicle.flags |= VehicleFlags.MOVED
            # Apply move function.
            x, _ = f(vehicle)
            if x < self.length:
                self.addPendingVehicle(vehicle=vehicle)
            else:
                self.removed.append(vehicle)
        self._commitLanes()

    def step(self) -> None:
        '''
        Performs a single simulation step moving all the vehicles.
        :return: None.
        '''
        self.removed = []
        self._updateLanes(lambda vehicle: vehicle.beforeMove())
        self._updateLanes(lambda vehicle: vehicle.move())


class CollisionError(RuntimeError):
    '''Raised when a collision on the road occurs.'''
    pass
