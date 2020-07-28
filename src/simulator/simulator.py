import typing
import random

from simulator.dispatcher.dispatcher import Dispatcher
from simulator.road.road import Road


class Hook:
    simulator: 'Simulator'

    def __init__(self, simulator: 'Simulator') -> None:
        self.simulator = simulator

    def __enter__(self) -> 'Hook':
        self.simulator.addHook(self)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.simulator.removeHook(self)

    def run(self) -> None:
        raise NotImplementedError()


class Simulator:
    road: Road
    dispatcher: Dispatcher
    steps: int
    hooks: typing.List[Hook]

    def __init__(self, road: Road, dispatcher: Dispatcher):
        self.road = road
        self.dispatcher = dispatcher
        self.steps = 0
        self.hooks = list()

    def scatterVehicles(self, density: float) -> None:
        '''
        Randomly scatters vehicles on the road with a desired density.
        :param density: probability a vehicle will be placed at every position.
        :return: None.
        '''
        for lane in range(self.road.lanes_count):
            for x in range(self.road.length):
                position = self.road.getRelativePosition(position=(x, lane))
                vehicle = self.dispatcher._newVehicle(position=position)
                if self.road.canPlaceVehicle(vehicle=vehicle) and random.random() < density:
                    self.road.addVehicle(vehicle=vehicle)

    def step(self) -> None:
        '''
        Performs a single step of the simulation.
        :return: None.
        '''
        self.dispatcher.dispatch()
        self.road.step()
        self.steps += 1
        for hook in self.hooks:
            hook.run()

    def addHook(self, hook: Hook) -> None:
        self.hooks.append(hook)

    def removeHook(self, hook: Hook) -> None:
        self.hooks.remove(hook)
