from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.car import Car
from simulator.vehicle.obstacle import Obstacle
from simulator.vehicle.vehicle import Vehicle
from util.rand import shuffled


class AutonomousCar(Car):
    def __init__(self, position: Position, velocity: int, road: Road,
                 length: int = 1, width: int = 1, limit: int = 0):
        super().__init__(
            position=position, velocity=velocity, road=road,
            length=length, width=width, limit=limit)

    def beforeMove(self) -> Position:
        self.path.append((self.position, self.velocity))
        self.last_position = self.position
        if not self._tryAvoidObstacle():
            self._tryChangeLanes()
        return self.position

    def move(self) -> Position:
        x, lane = self.position
        self.velocity = min(self.velocity + 1, self._getMaxSpeed(position=self.position))
        self.position = x + self.velocity, lane
        return self.position

    def _tryAvoidObstacle(self) -> bool:
        x, lane = self.position
        vx, vehicle = self.road.getNextVehicle(position=self.position)
        if vehicle is None or not isinstance(vehicle, Obstacle):
            return False
        if vx - x > max(self.velocity, 1):
            return False
        # Find the best lane change.
        best_change = 0
        best_limit = self._getMaxSpeed(position=self.position)
        for change in shuffled([-self.road.lane_width, self.road.lane_width]):
            destination = (x, lane + change)
            if self._canAvoidObstacle(obstacle=vehicle, destination=destination):
                limit = self._getMaxSpeed(position=destination)
                if limit > best_limit:
                    best_change, best_limit = change, limit
        # Change to the best possible lane.
        if best_change != 0:
            destination = (x, lane + best_change)
            self._avoidObstacle(obstacle=vehicle, destination=destination)
            self.position = destination
            return True
        return False

    def _tryChangeLanes(self) -> bool:
        # Find the best lane change.
        x, lane = self.position
        best_change = 0
        best_limit = self._getMaxSpeed(position=self.position)
        for change in shuffled([-self.road.lane_width, self.road.lane_width]):
            destination = (x, lane + change)
            if self._canChangeLane(destination):
                limit = self._getMaxSpeed(position=destination)
                if limit > best_limit:
                    best_change, best_limit = change, limit
        if best_change != 0:
            self.position = (x, lane + best_change)
            return True
        return False

    def _getMaxSpeedBonus(self, next: Vehicle, position: Position) -> int:
        if isinstance(next, AutonomousCar):
            return next.velocity
        return 0

    def _getSafeChangeDistance(self, previous: Vehicle, destination: Position) -> int:
        if isinstance(previous, AutonomousCar):
            return previous.velocity
        return super()._getSafeChangeDistance(previous, destination)


def isAutonomous(vehicle: Vehicle) -> bool:
    return isinstance(vehicle, AutonomousCar)
