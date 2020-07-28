from simulator.road.road import Road
from simulator.simulator import Hook, Simulator
from simulator.statistics.averageresult import AverageResult
from simulator.statistics.velocity import getAverageVelocityFiltered
from simulator.vehicle.autonomous import isAutonomous
from simulator.vehicle.car import isCar
from simulator.vehicle.conventional import isConventional
from util.cumulativelist import CumulativeList


class Tracker(Hook):
    steps: int
    velocity: CumulativeList[AverageResult]
    velocity_autonomous: CumulativeList[AverageResult]
    velocity_conventional: CumulativeList[AverageResult]

    def __init__(self, simulator: Simulator, buffer_size: int = 1):
        super().__init__(simulator=simulator)
        self.steps = 0
        self.velocity = CumulativeList(size=buffer_size)
        self.velocity.append(AverageResult(0, 0))
        self.velocity_autonomous = CumulativeList(size=buffer_size)
        self.velocity_autonomous.append(AverageResult(0, 0))
        self.velocity_conventional = CumulativeList(size=buffer_size)
        self.velocity_conventional.append(AverageResult(0, 0))

    def run(self) -> None:
        self.steps += 1
        velocity = getAverageVelocityFiltered(self._road, isCar)
        velocity_autonomous = getAverageVelocityFiltered(self._road, isAutonomous)
        velocity_conventional = getAverageVelocityFiltered(self._road, isConventional)
        self.velocity.append(velocity)
        self.velocity_autonomous.append(velocity_autonomous)
        self.velocity_conventional.append(velocity_conventional)

    @property
    def _road(self) -> Road:
        return self.simulator.road
