from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.car import Car
from simulator.vehicle.vehicle import Vehicle


class AutonomousCar(Car):
    def __init__(self, position: Position, velocity: int, road: Road, length: int = 1):
        super().__init__(position=position, velocity=velocity, road=road, length=length)

    def beforeMove(self) -> Position:
        self.path.append((self.position, self.velocity))
        self.last_position = self.position
        x, lane = self.position
        # Find the best lane change.
        best_change = 0
        best_limit = self._getMaxSpeed(position=self.position)
        for change in [-1, 1]:
            destination = (x, lane + change)
            if self._changeLane(destination):
                limit = self._getMaxSpeed(position=destination)
                if limit > best_limit:
                    best_change, best_limit = change, limit
        # Switch the lanes.
        self.position = x, lane + best_change
        return self.position

    def move(self) -> Position:
        x, lane = self.position
        self.velocity = min(self.velocity + 1, self._getMaxSpeed(position=self.position))
        self.position = x + self.velocity, lane
        return self.position

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
