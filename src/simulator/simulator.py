from simulator.dispatcher.dispatcher import Dispatcher
from simulator.road.road import Road


class Simulator:
    road: Road
    dispatcher: Dispatcher

    def __init__(self, road: Road, dispatcher: Dispatcher):
        self.road = road
        self.dispatcher = dispatcher

    def step(self) -> None:
        '''
        Performs a single step of the simulation.
        :return: None.
        '''
        self.dispatcher.dispatch()
        self.road.step()
        print(f'Average velocity: {self.road.getAverageVelocity()}')
