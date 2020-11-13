import itertools
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
    emergency: typing.Set[Vehicle]

    def __init__(self, length: int, lanes_count: int, lane_width: int,
                 controller: typing.Optional[SpeedController] = None):
        self.length = length
        self.lanes_count = lanes_count
        self.lane_width = lane_width
        self.controller = controller if controller is not None else SpeedController()
        self.removed = list()
        self.emergency = set()

    @property
    def sublanesCount(self) -> int:
        '''
        Returns the actual sub-lanes count.
        :return: number of sub-lanes.
        '''
        return self.lanes_count * self.lane_width + self.lane_width // 2 * 2

    @property
    def emergencyLane(self) -> int:
        '''
        Returns the index of an emergency sub-lane start.
        :return: index of an emergency sub-lane.
        '''
        return self.lane_width

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

    def isSingleLane(self, vehicle: Vehicle) -> bool:
        '''
        Checks if a given vehicle is occupying a single lane.
        :param vehicle: a vehicle to check.
        :return: whether it occupies a single lane.
        '''
        x, lane = vehicle.position
        _, start = self.getAbsolutePosition(position=vehicle.position)
        _, end = self.getAbsolutePosition(position=(x, lane + vehicle.width - 1))
        return start == end

    def addVehicle(self, vehicle: Vehicle) -> None:
        '''
        Adds a new vehicle to the road.
        :param position: position on the road.
        :param vehicle: vehicle to add.
        :return: None.
        '''
        raise NotImplementedError()

    def addEmergencyVehicle(self, vehicle: Vehicle) -> None:
        '''
        Adds a new emergency vehicle to the  road.
        :param vehicle: vehicle to add.
        :return: None.
        '''
        if not vehicle.flags & VehicleFlags.EMERGENCY:
            raise ValueError('emergency vehicle expected')
        self.emergency.add(vehicle)
        self.addVehicle(vehicle=vehicle)

    def getVehicle(self, position: Position) -> typing.Optional[Vehicle]:
        '''
        Gets a vehicle from the road.
        :param position: position on the road.
        :return: a vehicle currently at the given position or None.
        '''
        raise NotImplementedError()

    def getAllActiveVehicles(self) -> typing.Generator[Vehicle, None, None]:
        '''
        Gets all the vehicles on the road.
        :return: generator yielding all the vehicles.
        '''
        raise NotImplementedError()

    def getAllVehicles(self) -> typing.Iterator[Vehicle]:
        '''
        Gets all vehicles on the road including recently removed vehicles.
        :return: generator yielding all the vehicles.
        '''
        return itertools.chain(self.getAllActiveVehicles(), self.removed)

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
        return inBounds(lane, 0, self.sublanesCount) and inBounds(x, 0, self.length)

    def isSafePosition(self, position: Position, ignore: typing.Optional[Vehicle] = None) -> bool:
        '''
        Checks if a position is safe to place a vehicle in.
        :param position: position on the road.
        :param ignore: ignore potential collisions with the given vehicle.
        :return: if a position is safe.
        '''
        if not self.isProperPosition(position=position):
            return False
        vehicle = self.getVehicle(position=position)
        pending = self.getPendingVehicle(position=position)
        return (vehicle is None or vehicle is ignore) and (pending is None or pending is ignore)

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
        for vehicle in self.getAllActiveVehicles():
            vehicle.flags &= ~VehicleFlags.MOVED

        for vehicle in self.getAllActiveVehicles():
            # Skip vehicles with MOVED flag set.
            if VehicleFlags.MOVED in vehicle.flags:
                continue
            vehicle.flags |= VehicleFlags.MOVED
            # Apply move function.
            x, _ = f(vehicle)
            if x < self.length:
                self.addPendingVehicle(vehicle=vehicle)
            else:
                self._removeVehicle(vehicle)
        self._commitLanes()

    def _removeVehicle(self, vehicle: Vehicle) -> None:
        '''
        Removes vehicle from the road.
        :param vehicle: vehicle to remove.
        :return: None.
        '''
        self.removed.append(vehicle)
        if vehicle.flags & VehicleFlags.EMERGENCY:
            self.emergency.remove(vehicle)

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
