import typing

from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.obstacle import Obstacle
from simulator.vehicle.vehicle import Vehicle


class Car(Vehicle):
    # Constants.
    EMERGENCY_RADIUS = 10

    # Car properties.
    road: Road
    limit: int

    # Runtime properties.
    path: typing.List[typing.Tuple[Position, int]]
    zipped: typing.Set[Vehicle]

    def __init__(self, position: Position, velocity: int, road: Road,
                 length: int = 1, width: int = 1, limit: int = 0):
        super().__init__(position=position, velocity=velocity, length=length, width=width)
        self.road = road
        self.limit = limit
        self.path = list()
        self.zipped = set()

    def _getMaxSpeedUnlimited(self, position: Position) -> int:
        '''
        Returns maximum speed a car can go without causing an accident, does not apply speed limits.
        :param position: position on the road.
        :return: maximum speed.
        '''
        x, lane = position
        speed = self.road.length
        for w in range(self.width):
            next, vehicle = self.road.getNextVehicle(position=(x, lane + w))
            if vehicle is not None:
                max_speed = next - x - 1 + self._getMaxSpeedBonus(next=vehicle, position=position)
                speed = min(speed, max_speed)
        return speed

    def _getMaxSpeed(self, position: Position) -> int:
        '''
        Returns maximum speed a car can go without breaking speed limits or causing an accident.
        :param position: position on the road.
        :return: maximum speed.
        '''
        limit = self.road.controller.getMaxSpeed(position=position, width=self.width) + self.limit
        speed = self._getMaxSpeedUnlimited(position=position)
        return max(min(limit, speed), 0)

    def _getMaxSpeedBonus(self, next: Vehicle, position: Position) -> int:
        '''
        Get a max speed bonus based on vehicle intercommunication.
        :param next: next vehicle.
        :param position: position on the road.
        :return: speed bonus.
        '''
        return 0

    def _isChangePossible(self, destination: Position) -> bool:
        '''
        Checks if a lane is not occupied at the whole length of a car.
        :param destination: position on the road.
        :return: if it is possible to change the lane.
        '''
        x, lane = destination
        return all(self.road.isSafePosition(position=(x - i, lane + w), ignore=self)
                   for i in range(self.length) for w in range(self.width))

    def _isChangeRequired(self) -> bool:
        '''
        Checks if the vehicle is not possible to accelerate on the current lane.
        :return: if it is possible to accelerate.
        '''
        return self._getMaxSpeedUnlimited(position=self.position) < self.velocity + 1

    def _isChangeBeneficial(self, destination: Position) -> bool:
        '''
        Checks if a vehicle will benefit from the lane change with a faster maximum velocity.
        :param destination: position on the road.
        :return: if it is beneficial to change the lane.
        '''
        destination_limit = self._getMaxSpeedUnlimited(position=destination)
        return destination_limit > self.velocity + 1

    def _isChangeSafe(self, destination: Position) -> bool:
        '''
        Check if the distance to the previous vehicle is large enough for change to be safe.
        :param destination: position on the road.
        :return: if it is safe to change the lane.
        '''
        x, _ = self.position
        previous, vehicle = self.road.getPreviousVehicle(position=destination)
        if vehicle is None:
            return True
        limit = self._getSafeChangeDistance(previous=vehicle, destination=destination)
        return x - (self.length - 1) - previous > limit

    def _getSafeChangeDistance(self, previous: Vehicle, destination: Position) -> int:
        '''
        Returns a safe distance to the previous vehicle to change a lane.
        :type previous: previous vehicle.
        :param destination: position on the road.
        :return: safe distance.
        '''
        return self.road.controller.getMaxSpeed(position=destination, width=self.width)

    def _canChangeLane(self, destination: Position, force: bool = False) -> bool:
        '''
        Returns whether to change the lane to destination.
        :param destination: position on the road.
        :param force: whether to force a non required change.
        :return: whether to change the lane.
        '''
        return \
            (force or self._isChangeRequired()) and \
            self._isChangePossible(destination=destination) and \
            self._isChangeBeneficial(destination=destination) and \
            self._isChangeSafe(destination=destination)

    def _canAvoid(self, obstacle: Vehicle, destination: Position) -> bool:
        '''
        Returns whether it is possible to change the lane to destination, avoiding an obstacle
        and zipping in front of another vehicle.
        :param destination: position on the road.
        :return: whether to change lane.
        '''
        # If there is no space in the destination lane return False.
        if not self._isChangePossible(destination=destination):
            return False
        # If there is a space and it is safe to switch return False.
        if self._isChangeSafe(destination=destination):
            return True

        # Specific strategies depend on a vehicle type on the destination lane.
        _, vehicle = self.road.getPreviousVehicle(position=destination)
        if vehicle is None:
            return True
        if isinstance(vehicle, Car):
            return not self.road.isSingleLane(vehicle) \
                   or obstacle not in vehicle.zipped
        elif isinstance(vehicle, Obstacle):
            return True

        # In case new vehicle types get added make sure we remember to add it here.
        assert False, 'unreachable'

    def _avoid(self, obstacle: Vehicle, destination: Position) -> None:
        '''
        Avoid given obstacle or vehicle by changing lane to the destination lane.
        :param obstacle: obstacle to avoid.
        :param destination: destination to change to.
        :return: None.
        '''
        # If it is safe to change the lane do not set any flags.
        if self._isChangeSafe(destination=destination):
            return
        # Vehicle is not None otherwise it is safe to change the lane.
        _, vehicle = self.road.getPreviousVehicle(position=destination)
        assert vehicle is not None, 'unreachable'
        # Zip in front of a different car.
        if isinstance(vehicle, Car):
            vehicle.zipped.add(obstacle)

    def _tryAvoidWithChange(self, obstacle: Vehicle, change: int) -> bool:
        '''
        Try avoiding an obstacle by changing a lane by a specified vector.
        :param obstacle: obstacle to avoid.
        :param change: lane change vector.
        :return: if lane was changed.
        '''
        x, lane = self.position
        destination = (x, lane + change)
        if self._canAvoid(obstacle=obstacle, destination=destination):
            self._avoid(obstacle=obstacle, destination=destination)
            self.position = destination
            return True
        return False

    def _tryChangeLanes(self) -> bool:
        '''
        Tries to change a lane for vehicle benefits.
        :return: whether a lane was changed.
        '''
        raise NotImplementedError

    def _tryAvoidObstacle(self) -> bool:
        '''
        Checks if an obstacle blocks the current lane and tries to avoid it.
        :return: whether a lane was changed.
        '''
        raise NotImplementedError

    def _tryChangeEmergency(self) -> bool:
        '''
        Tries to change a lane to make space for an emergency vehicle.
        :return: whether a lane was changed.
        '''
        raise NotImplementedError

    def _getEmergency(self) -> typing.Optional[Vehicle]:
        '''
        Checks if an emergency vehicle is approaching.
        :return: whether an emergency vehicle is approaching.
        '''
        x, _ = self.position
        for emergency in self.road.emergency:
            ex, _ = emergency.position
            if abs(x - ex) < Car.EMERGENCY_RADIUS:
                return emergency
        return None

    def beforeMove(self) -> Position:
        self.path.append((self.position, self.velocity))
        self.last_position = self.position
        changes = [
            lambda: self._tryAvoidObstacle(),
            lambda: self._tryChangeEmergency(),
            lambda: self._tryChangeLanes(),
        ]
        for tryChange in changes:
            if tryChange():
                break
        return self.position


def isCar(vehicle: Vehicle) -> bool:
    return isinstance(vehicle, Car)
