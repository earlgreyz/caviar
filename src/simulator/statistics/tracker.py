import typing

from simulator.road.road import Road
from simulator.simulator import Hook, Simulator
from simulator.statistics.averageresult import AverageResult
from simulator.statistics.decelerations import getDecelerations
from simulator.statistics.lanechanges import getLaneChanges
from simulator.statistics.velocity import getAverageVelocityFiltered
from simulator.statistics.waiting import getWaiting
from simulator.vehicle.autonomous import isAutonomous
from simulator.vehicle.car import isCar
from simulator.vehicle.conventional import isConventional
from util.cumulativelist import CumulativeList
from util.format import OptionalFormat


class Tracker(Hook):
    steps: int
    velocity: CumulativeList[AverageResult]
    velocity_autonomous: CumulativeList[AverageResult]
    velocity_conventional: CumulativeList[AverageResult]
    decelerations: CumulativeList[int]
    lane_changes: CumulativeList[int]
    waiting: CumulativeList[int]

    def __init__(self, simulator: Simulator, buffer_size: int = 1):
        super().__init__(simulator=simulator)
        self.steps = 0
        self.velocity = CumulativeList(buffer_size, AverageResult(0, 0))
        self.velocity_autonomous = CumulativeList(buffer_size, AverageResult(0, 0))
        self.velocity_conventional = CumulativeList(buffer_size, AverageResult(0, 0))
        self.decelerations = CumulativeList(buffer_size, 0)
        self.lane_changes = CumulativeList(buffer_size, 0)
        self.waiting = CumulativeList(buffer_size, 0)

    @property
    def _road(self) -> Road:
        return self.simulator.road

    def run(self) -> None:
        self.steps += 1
        velocity = getAverageVelocityFiltered(self._road, isCar)
        velocity_autonomous = getAverageVelocityFiltered(self._road, isAutonomous)
        velocity_conventional = getAverageVelocityFiltered(self._road, isConventional)
        self.velocity.append(velocity)
        self.velocity_autonomous.append(velocity_autonomous)
        self.velocity_conventional.append(velocity_conventional)
        self.decelerations.append(getDecelerations(self._road))
        self.lane_changes.append(getLaneChanges(self._road))
        self.waiting.append(getWaiting(self._road))

    def getVelocity(self) -> typing.Optional[float]:
        return self.velocity.value().toMaybeFloat()

    def getVelocityAutonomous(self) -> typing.Optional[float]:
        return self.velocity_autonomous.value().toMaybeFloat()

    def getVelocityConventional(self) -> typing.Optional[float]:
        return self.velocity_conventional.value().toMaybeFloat()

    def getDecelerations(self) -> float:
        return self.decelerations.value() / len(self.decelerations)

    def getLaneChanges(self) -> float:
        return self.lane_changes.value() / len(self.lane_changes)

    def getWaiting(self) -> float:
        return self.waiting.value() / len(self.waiting)

    def getCSV(self) -> str:
        def fmt(x: typing.Optional[float]) -> str:
            return '{:.2f}'.format(OptionalFormat(x))

        statistics = {
            'velocity': self.getVelocity(),
            'velocity_autonomous': self.getVelocityAutonomous(),
            'velocity_conventional': self.getVelocityAutonomous(),
            'decelerations': self.getDecelerations(),
            'lane_changes': self.getLaneChanges(),
            'waiting': self.getWaiting()
        }
        return ','.join(statistics.keys()) + '\n' + ','.join(map(fmt, statistics.values()))
