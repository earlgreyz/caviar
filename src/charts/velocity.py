import os
import typing

import click
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt

VelocityData = typing.List[typing.List[float]]


class VelocityChart:
    car: pd.DataFrame
    autonomous: pd.DataFrame
    conventional: pd.DataFrame

    def __init__(self, car: VelocityData, autonomous: VelocityData, conventional: VelocityData):
        self.car = pd.DataFrame(car)
        self.autonomous = pd.DataFrame(autonomous)
        self.conventional = pd.DataFrame(conventional)

    def plot(self) -> None:
        click.secho('Average speed', fg='yellow')
        print(self.car.to_csv())
        click.secho('Autonomous speed', fg='yellow')
        print(self.autonomous.to_csv())
        click.secho('Conventional speed', fg='yellow')
        print(self.conventional.to_csv())
        plt.show()

    def save(self, path: str, prefix: str) -> None:
        car_path = os.path.join(path, f'{prefix}_car.csv')
        self.car.to_csv(car_path)
        autonomous_path = os.path.join(path, f'{prefix}_autonomous.csv')
        self.autonomous.to_csv(autonomous_path)
        conventional_path = os.path.join(path, f'{prefix}_conventional.csv')
        self.conventional.to_csv(conventional_path)
        self._prepareChart()
        plt_path = os.path.join(path, f'{prefix}.png')
        plt.savefig(plt_path, bbox_inches='tight')

    def _prepareChart(self) -> None:
        sns.set_style('darkgrid')
        data = pd.DataFrame({
            'All': self.car.sum(axis=0) / self.car.shape[0],
            'Autonomous': self.autonomous.sum(axis=0) / self.autonomous.shape[0],
            'Conventional': self.conventional.sum(axis=0) / self.conventional.shape[0]})
        ax = sns.lineplot(data=data)
        ax.set(ylabel='Speed', xlabel='Position', title='Average speed on the road\n')
