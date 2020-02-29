from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.vehicle import Vehicle


class AutonomousCar(Vehicle):
    road: Road

    def __init__(self, position: Position, velocity: int, road: Road):
        super().__init__(position=position, velocity=velocity)
        self.road = road

    def beforeMove(self) -> Position:
        self.last_position = self.position
        x, lane = self.position
        # Find the best lane change.
        best_change = 0
        best_limit = self._getMaxSpeed(position=self.position)
        for change in [-1, 1]:
            destination = (x, lane + change)
            if not self._canChangeLane(destination) or not self._shouldChangeLane(destination):
                continue
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

    def _canChangeLane(self, destination: Position) -> bool:
        return self.road.isProperPosition(position=destination) and \
               self.road.getVehicle(position=destination) is None

    def _shouldChangeLane(self, destination: Position) -> bool:
        x, _ = self.position
        # Check if the speed limit on the destination lane is higher.
        limit = self._getMaxSpeed(self.position)
        destination_limit = self._getMaxSpeed(position=destination)
        if destination_limit <= limit:
            return False
        return True

    def _getMaxSpeed(self, position: Position) -> int:
        x, _ = position
        limit = self.road.controller.getMaxSpeed(position=position)
        next, vehicle = self.road.getNextVehicle(position=position)
        if vehicle is None:
            return limit
        distance = next - x
        if isinstance(vehicle, AutonomousCar):
            distance += vehicle.velocity
        return min(limit, distance - 1)


def isAutonomous(vehicle: Vehicle) -> bool:
    return isinstance(vehicle, AutonomousCar)
