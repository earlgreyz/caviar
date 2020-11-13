import random
import typing

from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.car import Car
from simulator.vehicle.obstacle import Obstacle
from simulator.vehicle.vehicle import Vehicle
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
                 length: int = 1, width: int = 1,
                 limit: int = 0, driver: MaybeDriver = None):
        super().__init__(
            position=position, velocity=velocity, road=road,
            length=length, width=width, limit=limit)
        self.driver = driver if driver is not None else Driver()

    def move(self) -> Position:
        # Don't move if the vehicle is not fully on a single lane.
        if not self.road.isSingleLane(self):
            return self.position

        x, lane = self.position
        if self.velocity > 0 and random.random() < self.driver.slow:
            self.velocity -= 1
        else:
            self.velocity += 1
        self.velocity = min(self.velocity, self._getMaxSpeed(position=self.position))
        self.position = x + self.velocity, lane
        return self.position

    def _tryAvoidObstacle(self) -> bool:
        '''
        Try changing the lane to avoid an obstacle.
        :return: if lane was changed.
        '''
        x, lane = self.position
        vx, vehicle = self.road.getNextVehicle(position=self.position)
        if vehicle is None or not isinstance(vehicle, Obstacle):
            return False
        if vx - x > max(self.velocity, 1):
            return False
        # Try to switch lanes in random order.
        for change in shuffled([-self.road.lane_width, self.road.lane_width]):
            if self._tryAvoidWithChange(obstacle=vehicle, change=change):
                return True
        return False

    def _tryChangeLanes(self) -> bool:
        '''
        Try changing the lane to improve speed.
        :return: if lane was changed.
        '''
        # Try to switch lanes in random order.
        x, lane = self.position
        for change in shuffled([-self.road.lane_width, self.road.lane_width]):
            destination = (x, lane + change)
            # Force changes for asymmetrical cases when switching from L -> R.
            force = change == 1 and not self.driver.symmetry
            if self._canChangeLane(destination=destination, force=force):
                self.position = destination
                return True
        return False

    def _tryChangeEmergency(self) -> bool:
        emergency = self._getEmergency()
        changeValue = self.road.lane_width // 2
        # If there is no emergency or already avoiding the emergency, continue.
        if emergency is None:
            if self.road.isSingleLane(self):
                return False
            else:
                _, absoluteLane = self.road.getAbsolutePosition(self.position)
                change = changeValue if absoluteLane == -1 else -changeValue
                # When coming back always get priority.
                return self._tryAvoidWithChange(Obstacle((-1, -1), 0, 0), change)

        # If already creating emergency corridor don't move.
        if not self.road.isSingleLane(self):
            return True
        # Decelerate slowly, cannot switch lanes when the speed is too high.
        self.velocity = max(1, self.velocity - 1)
        if self.velocity > 2:
            return True
        # Destination lane depends on the road position.
        _, absoluteLane = self.road.getAbsolutePosition(self.position)
        change = -changeValue if absoluteLane == 0 else changeValue
        self._tryAvoidWithChange(emergency, change)
        return True

    def _tryAvoidWithChange(self, obstacle: Vehicle, change: int) -> bool:
        x, lane = self.position
        destination = (x, lane + change)
        if self._canAvoid(obstacle=obstacle, destination=destination):
            self._avoid(obstacle=obstacle, destination=destination)
            self.position = destination
            return True
        return False

    def _canChangeLane(self, destination: Position, force: bool = False) -> bool:
        change_lane = super()._canChangeLane(destination=destination, force=force)
        return change_lane and random.random() < self.driver.change


def isConventional(vehicle: Vehicle) -> bool:
    return isinstance(vehicle, ConventionalCar)
