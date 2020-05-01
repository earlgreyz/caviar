import typing

from simulator.position import Position, inBounds
from simulator.road.speedcontroller import SpeedController
from simulator.statistics import Filter, AverageResult
from simulator.vehicle.vehicle import Vehicle, VehicleFlags


class Road:
    controller: SpeedController

    # Road options.
    length: int
    lanes_count: int

    emergency: typing.Set[Vehicle]
    removed: typing.List[Vehicle]

    # Constants.
    EMERGENCY_LANE: int = 1

    def __init__(self, length: int, lanes_count: int,
                 controller: typing.Optional[SpeedController] = None):
        self.length = length
        self.lanes_count = lanes_count
        self.controller = controller if controller is not None else SpeedController()
        self.removed = list()
        self.emergency = set()

    def addVehicle(self, vehicle: Vehicle) -> None:
        '''
        Adds a new vehicle to the road.
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
        if not vehicle.isEmergencyVehicle():
            raise ValueError('adding non emergency vehicle not allowed')
        self.emergency.add(vehicle)
        self.addVehicle(vehicle=vehicle)

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
        return inBounds(lane, 0, self.lanes_count) and inBounds(x, 0, self.length)

    def isSafePosition(self, position: Position) -> bool:
        '''
        Checks if a position is safe to place a vehicle in.
        :param position: position on the  road.
        :return: if a position is safe.
        '''
        return \
            self.isProperPosition(position=position) and \
            self.getVehicle(position=position) is None and \
            self.getPendingVehicle(position=position) is None

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
                self._removeVehicle(vehicle=vehicle)
        self._commitLanes()

    def _removeVehicle(self, vehicle: Vehicle) -> None:
        self.removed.append(vehicle)
        if vehicle.isEmergencyVehicle():
            self.emergency.remove(vehicle)

    def step(self) -> None:
        '''
        Performs a single simulation step moving all the vehicles.
        :return: None.
        '''
        self.removed = []
        self._updateLanes(lambda vehicle: vehicle.beforeMove())
        self._updateLanes(lambda vehicle: vehicle.move())

    def getAverageVelocityFiltered(self, predicate: Filter) -> AverageResult:
        velocity, count = 0, 0
        for vehicle in filter(predicate, self.getAllVehicles()):
            velocity += vehicle.velocity
            count += 1
        return AverageResult(value=velocity, count=count)

    def getAverageVelocity(self) -> AverageResult:
        return self.getAverageVelocityFiltered(lambda _: True)


class CollisionError(RuntimeError):
    '''Raised when a collision on the road occurs.'''
    pass
