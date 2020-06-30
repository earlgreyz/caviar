import typing

from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.vehicle import Vehicle


class Car(Vehicle):
    road: Road
    path: typing.List[typing.Tuple[Position, int]]
    limit: int

    def __init__(self, position: Position, velocity: int, road: Road,
                 length: int = 1, limit: int = 0):
        super().__init__(position=position, velocity=velocity, length=length)
        self.road = road
        self.path = []
        self.limit = limit

    def _getMaxSpeedUnlimited(self, position: Position) -> int:
        '''
        Returns maximum speed a car can go without causing an accident, does not apply speed limits.
        :param position: position on the road.
        :return: maximum speed.
        '''
        x, _ = position
        next, vehicle = self.road.getNextVehicle(position=position)
        if vehicle is None:
            return self.road.controller.getMaxSpeed(position=position) + 2
        return next - x - 1 + self._getMaxSpeedBonus(next=vehicle, position=position)

    def _getMaxSpeed(self, position: Position) -> int:
        '''
        Returns maximum speed a car can go without breaking speed limits or causing an accident.
        :param position: position on the road.
        :return: maximum speed.
        '''
        limit = self.road.controller.getMaxSpeed(position=position) + self.limit
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
        return all(self.road.isSafePosition(position=(x - i, lane)) for i in range(self.length))

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
        return self.road.controller.getMaxSpeed(position=destination)

    def _changeLane(self, destination: Position, force: bool = False) -> bool:
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


def isCar(vehicle: Vehicle) -> bool:
    return isinstance(vehicle, Car)
