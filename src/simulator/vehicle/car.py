import random
import typing

from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.vehicle import Vehicle


class CarParams:
    LANE_CHANGE_PROBABILITY: float
    SLOW_DOWN_PROBABILITY: float

    def __init__(self, change: float = .5, slow: float = .5):
        self.LANE_CHANGE_PROBABILITY = change
        self.SLOW_DOWN_PROBABILITY = slow


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
        if self._changeLane(destination=(x, lane + 1)):
            self.position = (x, lane + 1)
        elif self._changeLane(destination=(x, lane - 1)):
            self.position = (x, lane - 1)
        return self.position

    def move(self) -> Position:
        x, lane = self.position
        if self.velocity > 0 and random.random() <= self.params.SLOW_DOWN_PROBABILITY:
            self.velocity -= 1
        else:
            self.velocity = min(self.velocity + 1, self.road.getMaxSpeed(position=self.position))
        self.position = x + self.velocity, lane
        return self.position

    def _changeLane(self, destination: Position) -> bool:
        x, _ = self.position
        # Check if it is possible to change the lane.
        if not self.road.isProperPosition(position=destination):
            return False
        if self.road.getVehicle(position=destination) is not None:
            return False
        # Check if the speed limit on the destination lane is higher.
        limit = self.road.getMaxSpeed(self.position)
        destination_limit = self.road.getMaxSpeed(position=destination)
        if destination_limit <= limit:
            return False
        # Check if the distance to the previous vehicle is not smaller than the velocity.
        next, vehicle = self.road.getNextVehicle(position=destination)
        if vehicle is not None:
            distance = x - next
            if distance <= vehicle.velocity:
                return False
        # Randomly decide to switch the lane.
        return random.random() <= self.params.LANE_CHANGE_PROBABILITY
