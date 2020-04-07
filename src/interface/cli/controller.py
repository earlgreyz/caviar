import click

from simulator.simulator import Simulator
from simulator.vehicle.car import Car


class Controller:
    simulator: Simulator

    def __init__(self, simulator: Simulator):
        self.simulator = simulator

    def run(self, steps: int, individual: bool):
        with click.progressbar(range(steps), steps) as bar:
            for _ in bar:
                statistics = self.simulator.step()
                if individual:
                    for vehicle in self.simulator.road.removed:
                        if isinstance(vehicle, Car):
                            print(vehicle.path)
                else:
                    print(statistics)
