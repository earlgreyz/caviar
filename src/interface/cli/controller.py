import click
import typing

from simulator.simulator import Simulator
from simulator.statistics import Statistics


class Controller:
    simulator: Simulator

    def __init__(self, simulator: Simulator):
        self.simulator = simulator

    def run(self, steps: int):
        ss: typing.List[Statistics] = []
        with click.progressbar(range(steps), steps) as bar:
            for _ in bar:
                statistics = self.simulator.step()
                ss.append(statistics)
        print(ss[-1]['average_velocity'])
