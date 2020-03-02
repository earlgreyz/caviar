import click
import typing

from simulator.simulator import Simulator
from simulator.statistics import Statistics


class Controller:
    simulator: Simulator

    def __init__(self, simulator: Simulator):
        self.simulator = simulator

    def run(self, steps: int):
        statistics: typing.List[Statistics] = []
        with click.progressbar(range(steps), steps) as bar:
            for _ in bar:
                statistics.append(self.simulator.step())
        print(statistics)
