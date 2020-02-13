from simulator.dispatcher.car import CarDispatcher
from simulator.road.road import Road


class Simulator:
    road: Road
    dispatcher: CarDispatcher

    def __init__(self, road: Road, dispatcher: CarDispatcher):
        self.road = road
        self.dispatcher = dispatcher

    def step(self):
        self.dispatcher.dispatch()
        self.road.step()
        print(f'Average velocity: {self.road.getAverageVelocity()}')
