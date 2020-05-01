import random
import typing

from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.car import Car
from simulator.vehicle.vehicle import Vehicle, VehicleFlags
from util.rand import shuffled


class Driver:
    change: float
    slow: float
    symmetry: bool

    def __init__(self, change: float = .1, slow: float = .05, symmetry: bool = True):
        self.change = change
        self.slow = slow
        self.symmetry = symmetry


MaybeDriver = typing.Optional[Driver]


class ConventionalCar(Car):
    driver: Driver

    def __init__(self, position: Position, velocity: int, road: Road,
                 length: int = 1, limit: int = 0, driver: MaybeDriver = None):
        super().__init__(
            position=position, velocity=velocity, road=road, length=length, limit=limit)
        self.driver = driver if driver is not None else Driver()

    def beforeMove(self) -> Position:
        self.path.append((self.position, self.velocity))
        self.last_position = self.position

        if self._isEmergency():
            return self.beforeEmergency()
        else:
            self.flags &= ~(VehicleFlags.CHANGED | VehicleFlags.NICE)

        x, lane = self.position
        # Try to switch lanes in random order.
        for change in shuffled([-1, 1]):
            destination = (x, lane + change)
            # Force changes for asymmetrical cases when switching from L -> R.
            force = change == 1 and not self.driver.symmetry
            if self._changeLane(destination=destination, force=force):
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

    def beforeEmergency(self) -> Position:
        x, lane = self.position
        # From emergency lane you can switch both ways.
        changes = [1]
        if lane == Road.EMERGENCY_LANE:
            changes = [-1, 1]

        for change in shuffled(changes):
            destination = (x, lane + change)
            if self._changeEmergency(destination=destination):
                self.position = destination
                self.flags &= VehicleFlags.CHANGED
                _, vehicle = self.road.getPreviousVehicle(position=destination)
                if vehicle is not None:
                    vehicle.flags &= VehicleFlags.NICE
                break
        return self.position

    def _changeLane(self, destination: Position, force: bool = False) -> bool:
        change_lane = super()._changeLane(destination=destination, force=force)
        return random.random() < self.driver.change and change_lane


def isConventional(vehicle: Vehicle) -> bool:
    return isinstance(vehicle, ConventionalCar)
