import random
import typing

from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.car import Car
from simulator.vehicle.vehicle import Vehicle
from util.rand import shuffled


class Driver:
    change: float
    slow: float

    def __init__(self, change: float = .25, slow: float = .25):
        self.change = change
        self.slow = slow


MaybeDriver = typing.Optional[Driver]


class ConventionalCar(Car):
    driver: Driver

    def __init__(self, position: Position, velocity: int, road: Road, length: int = 1,
                 driver: MaybeDriver = None):
        super().__init__(position=position, velocity=velocity, length=length, road=road)
        self.driver = driver if driver is not None else Driver()

    def beforeMove(self) -> Position:
        self.path.append((self.position, self.velocity))
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
        if self.velocity > 0 and random.random() < self.driver.slow:
            self.velocity -= 1
        else:
            self.velocity += 1
        self.velocity = min(self.velocity, self._getMaxSpeed(position=self.position))
        self.position = x + self.velocity, lane
        return self.position

    def _changeLane(self, destination: Position) -> bool:
        change_lane = super()._changeLane(destination=destination)
        return random.random() < self.driver.change and change_lane


def isConventional(vehicle: Vehicle) -> bool:
    return isinstance(vehicle, ConventionalCar)
