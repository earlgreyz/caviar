from simulator.dispatcher.dispatcher import Dispatcher
from simulator.road.road import Road
from simulator.statistics import Statistics, Filter, combine, filterLane
from simulator.vehicle.autonomous import isAutonomous
from simulator.vehicle.car import isCar
from simulator.vehicle.conventional import isConventional


class Simulator:
    road: Road
    dispatcher: Dispatcher
    steps: int

    def __init__(self, road: Road, dispatcher: Dispatcher):
        self.road = road
        self.dispatcher = dispatcher
        self.steps = 0

    def step(self) -> Statistics:
        '''
        Performs a single step of the simulation.
        :return: None.
        '''
        self.dispatcher.dispatch()
        self.road.step()
        self.steps += 1
        return dict(
            average_velocity=self.road.getAverageVelocityFiltered(isCar),
            average_velocity_autonomous=self.road.getAverageVelocityFiltered(isAutonomous),
            average_velocity_conventional=self.road.getAverageVelocityFiltered(isConventional),
            steps=self.steps,
            throughput=len(self.road.removed),
            lanes={
                lane: self._getStatisticsFiltered(filterLane(lane))
                for lane in range(self.road.lanes_count)
            }
        )

    def _getStatisticsFiltered(self, *predicates: Filter) -> Statistics:
        return dict(
            average_velocity=self.road.getAverageVelocityFiltered(
                combine(*predicates, isCar)),
            average_velocity_autonomous=self.road.getAverageVelocityFiltered(
                combine(*predicates, isAutonomous)),
            average_velocity_conventional=self.road.getAverageVelocityFiltered(
                combine(*predicates, isConventional)),
        )
