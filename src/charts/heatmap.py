import os
import typing

import click
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt

HeatMapData = typing.List[typing.List[float]]


class HeatMap:
    data: pd.DataFrame
    title: str
    max_value: float

    def __init__(self, data: HeatMapData, title: str, max_value: float):
        self.data = pd.DataFrame(data=data)
        self.title = title
        self.max_value = max_value

    def plot(self) -> None:
        click.secho(self.title, fg='yellow')
        print(self.data.to_csv())
        self._prepareChart()
        plt.show()

    def save(self, path: str, prefix: str) -> None:
        csv_path = os.path.join(path, f'{prefix}.csv')
        self.data.to_csv(csv_path)
        self._prepareChart()
        plt_path = os.path.join(path, f'{prefix}.png')
        plt.savefig(plt_path, bbox_inches='tight')

    def _prepareChart(self) -> None:
        sns.set_style('darkgrid')
        length = len(self.data[0])

        # Set up the subplot grid
        f = plt.figure(figsize=(6, 4))
        gs = plt.GridSpec(10, 10, hspace=0)

        ax_heatmap = f.add_subplot(gs[4:, :])
        ax_plot = f.add_subplot(gs[:4, :], sharex=ax_heatmap)

        plt.setp(ax_heatmap.yaxis.get_majorticklines(), visible=False)
        plt.setp(ax_heatmap.get_yticklabels(), visible=False)

        plt.setp(ax_plot.get_xticklabels(), visible=False)
        plt.setp(ax_plot.xaxis.get_majorticklines(), visible=False)
        plt.setp(ax_plot.xaxis.get_minorticklines(), visible=False)

        # Make the grid look nice
        sns.utils.despine(f)
        sns.utils.despine(ax=ax_plot, left=True)
        f.tight_layout()

        plt.sca(ax_heatmap)
        N = 10
        xticks = [(length // N) * i for i in range(N + 1)]
        sns.heatmap(self.data, linewidth=0.01,
                    cbar_kws=dict(orientation='horizontal', shrink=.75, aspect=25, pad=.2))
        ax_heatmap.set_xticks(xticks)
        ax_heatmap.set_xticklabels(xticks)
        ax_heatmap.set(ylabel='Lane')

        plt.sca(ax_plot)
        ax_plot.set(xlabel=None, ylabel=None, ylim=(0, self.max_value), title=f'{self.title}\n')
        sns.lineplot(data=self.data.sum(axis=0))
