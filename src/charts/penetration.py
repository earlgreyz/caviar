import os

import click
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import typing


def make_plot(df: pd.DataFrame, key: str, title: str, ylabel: str, output, prefix) -> None:
    # Prepare data.
    key_all = f'{key}_all'
    data_all = df[['x', key_all]] \
        .rename(columns={key_all: 'y'})
    data_all['type'] = 'All'
    key_conventional = f'{key}_conventional'
    data_conventional = df[['x', key_conventional]] \
        .rename(columns={key_conventional: 'y'})
    data_conventional['type'] = 'Conventional'
    key_autonomous = f'{key}_autonomous'
    data_autonomous = df[['x', key_autonomous]] \
        .rename(columns={key_autonomous: 'y'})
    data_autonomous['type'] = 'Autonomous'
    data = data_all.append(data_conventional).append(data_autonomous)
    # Make plot.
    sns.set_style('darkgrid')
    f = plt.figure(figsize=(6, 4))
    f.tight_layout()
    g = sns.lineplot(x='x', y='y', hue='type', data=data)
    # Set axis title.
    g.set(xlabel='Market Penetration Rate', ylabel=ylabel, title=f'{title}\n')
    # Remove legend title.
    handles, labels = g.get_legend_handles_labels()
    g.legend(handles=handles[1:], labels=labels[1:])

    if output is not None:
        plt_path = os.path.join(output, f'{prefix}_{key}.png')
        plt.savefig(plt_path, bbox_inches='tight')
    else:
        plt.show()


@click.command()
@click.option('--output', '-o', default=None, help='Save output to a directory')
@click.option('--prefix', '-p', default='', help='Prefix for output file names')
@click.argument('file', type=click.File())
def main(output: typing.Optional[str], prefix: str, file):
    df = pd.read_csv(file, header=0)
    keys = ['velocity', 'throughput', 'decelerations', 'laneChanges', 'waiting']
    titles = ['Average speed',
              'Average Throughput per Step',
              'Average Number of Quick Decelerations per Step',
              'Average Number of Lane Changes per Step',
              'Number of Waiting Vehicles per Step']
    ylabels = ['Speed', 'Throughput / Step', 'Decelerations / Step',
               'Lane Changes / Step', 'Waiting Vehicles / Step']
    for key, title, ylabel in zip(keys, titles, ylabels):
        make_plot(df, key, title, ylabel, output, prefix)


if __name__ == '__main__':
    main()
