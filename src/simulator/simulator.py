import typing

from simulator.dispatcher.dispatcher import Dispatcher
from simulator.road.road import Road
from simulator.statistics import AverageResult, Statistics, combine, filterLane
from simulator.vehicle.autonomous import isAutonomous
from simulator.vehicle.car import isCar
from simulator.vehicle.conventional import isConventional
from util.cumulativelist import CumulativeList


class Simulator:
    road: Road
    dispatcher: Dispatcher
    steps: int

    # Statistics, storing cumulative sums to calculate results quickly.
    velocity: typing.List[CumulativeList[AverageResult]]
    velocity_autonomous: typing.List[CumulativeList[AverageResult]]
    velocity_conventional: typing.List[CumulativeList[AverageResult]]
    throughput: CumulativeList[int]

    def __init__(self, road: Road, dispatcher: Dispatcher, buffer_size: int = 1):
        self.road = road
        self.dispatcher = dispatcher
        self.steps = 0

        # Initialize statistics lists.
        self.velocity = \
            [CumulativeList(buffer_size) for _ in range(road.lanes_count + 1)]
        self.velocity_autonomous = \
            [CumulativeList(buffer_size) for _ in range(road.lanes_count + 1)]
        self.velocity_conventional = \
            [CumulativeList(buffer_size) for _ in range(road.lanes_count + 1)]
        self.throughput = CumulativeList(buffer_size)

    def step(self) -> Statistics:
        '''
        Performs a single step of the simulation.
        :return: None.
        '''
        self.dispatcher.dispatch()
        self.road.step()
        self.steps += 1
        # Gather statistics.
        for lane in range(self.road.lanes_count + 1):
            self._gatherLaneStatistics(lane)
        self.throughput.append(len(self.road.removed))
        # Return statistics.
        return dict(
            **self._getLaneStatistics(self.road.lanes_count),
            steps=self.steps,
            throughput=float(self.throughput.value()) / len(self.throughput),
            lanes={
                lane: self._getLaneStatistics(lane) for lane in range(self.road.lanes_count)
            }
        )

    def _gatherLaneStatistics(self, lane: int) -> None:
        predicates = [] if lane == self.road.lanes_count else [filterLane(lane)]
        # Gather statistics.
        velocity = self.road.getAverageVelocityFiltered(combine(*predicates, isCar))
        velocity_autonomous = self.road.getAverageVelocityFiltered(
            combine(*predicates, isAutonomous))
        velocity_conventional = self.road.getAverageVelocityFiltered(
            combine(*predicates, isConventional))
        # Calculate cumulative sums.
        self.velocity[lane].append(velocity)
        self.velocity_autonomous[lane].append(velocity_autonomous)
        self.velocity_conventional[lane].append(velocity_conventional)

    def _getLaneStatistics(self, lane: int) -> Statistics:
        return dict(
            average_velocity=self.velocity[lane].value().toMaybeFloat(),
            average_velocity_conventional=self.velocity_conventional[lane].value().toMaybeFloat(),
            average_velocity_autonomous=self.velocity_autonomous[lane].value().toMaybeFloat(),
        )
