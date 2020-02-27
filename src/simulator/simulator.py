from simulator.dispatcher.dispatcher import Dispatcher
from simulator.road.road import Road
from simulator.statistics import Statistics
from simulator.vehicle.autonomous import isAutonomous
from simulator.vehicle.car import isConventional


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
            average_velocity=self.road.getAverageVelocity(),
            average_velocity_autonomous=self.road.getAverageVelocityFiltered(isAutonomous),
            average_velocity_conventional=self.road.getAverageVelocityFiltered(isConventional),
            steps=self.steps,
        )
