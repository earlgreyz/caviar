import random
import typing

from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.vehicle import Vehicle
from util.rand import shuffled


class CarParams:
    lane_change_probability: float
    slow_down_probability: float

    def __init__(self, change: float = .5, slow: float = .2):
        self.lane_change_probability = change
        self.slow_down_probability = slow


class Car(Vehicle):
    params: CarParams
    road: Road

    def __init__(self, position: Position, velocity: int, road: Road,
                 params: typing.Optional[CarParams] = None):
        super().__init__(position=position, velocity=velocity)
        self.road = road
        self.params = params if params is not None else CarParams()

    def beforeMove(self) -> Position:
        self.last_position = self.position
        x, lane = self.position
        # Try to switch lanes in random order.
        for change in shuffled([-1, 1]):
            destination = (x, lane + change)
            if self._changeLane(destination):
                self.position = destination
                break
        return self.position

    def move(self) -> Position:
        x, lane = self.position
        if self.velocity > 0 and random.random() <= self.params.slow_down_probability:
            self.velocity -= 1
        else:
            self.velocity += 1
        self.velocity = min(self.velocity, self.road.getMaxSpeed(position=self.position))
        self.position = x + self.velocity, lane
        return self.position

    def _canChangeLane(self, destination: Position) -> bool:
        return self.road.isProperPosition(position=destination) and \
               self.road.getVehicle(position=destination) is None

    def _shouldChangeLane(self, destination: Position) -> bool:
        x, _ = self.position
        # Check if the speed limit on the destination lane is higher.
        limit = self.road.getMaxSpeed(self.position)
        destination_limit = self.road.getMaxSpeed(position=destination)
        if destination_limit <= limit:
            return False
        # Check if the distance to the previous vehicle is not smaller than the velocity.
        next, vehicle = self.road.getNextVehicle(position=destination)
        if vehicle is not None:
            if next - x <= self.velocity:
                return False
        return True

    def _changeLane(self, destination: Position) -> bool:
        if not self._canChangeLane(destination) or not self._shouldChangeLane(destination):
            return False
        return random.random() <= self.params.lane_change_probability


def isConventional(vehicle: Vehicle) -> bool:
    return isinstance(vehicle, Car)
