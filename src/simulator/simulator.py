from simulator.dispatcher.dispatcher import Dispatcher
from simulator.road.road import Road
from simulator.statistics import Statistics


class Simulator:
    road: Road
    dispatcher: Dispatcher

    def __init__(self, road: Road, dispatcher: Dispatcher):
        self.road = road
        self.dispatcher = dispatcher

    def step(self) -> Statistics:
        '''
        Performs a single step of the simulation.
        :return: None.
        '''
        self.dispatcher.dispatch()
        self.road.step()
        return self.road.getStatistics()
