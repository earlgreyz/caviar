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
            if self._canAvoid(obstacle=vehicle, destination=destination):
                limit = self._getMaxSpeed(position=destination)
                if limit > best_limit:
                    best_change, best_limit = change, limit
        # Change to the best possible lane.
        if best_change != 0:
            destination = (x, lane + best_change)
            self._avoid(obstacle=vehicle, destination=destination)
            self.position = destination
            return True
        return False

    def _tryChangeEmergency(self) -> bool:
        '''
        Try changing the lane to create an emergency corridor.
        :return: if vehicle performed an emergency action.
        '''
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
