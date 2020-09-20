import os

import click
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import typing


def make_plot(df: pd.DataFrame, key: str, ylabel: str, multiplier: int, ylim: int,
              output, prefix) -> None:
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
    data['y'] *= multiplier
    # Make plot.
    colors = sns.color_palette(['#000', '#000', '#000'])
    sns.set(font='serif', style='white', rc={'text.usetex': True})
    f = plt.figure(figsize=(6, 4))
    f.tight_layout()
    g = sns.lineplot(x='x', y='y', hue='type', data=data, err_style='bars', palette=colors)
    # Set axis title.
    g.set(xlabel='Market Penetration Rate ($\%$)', ylabel=ylabel, ylim=(0., ylim))  # noqa: W605
    # Change the lines style.
    g.lines[2].set_linestyle('--')
    g.lines[4].set_linestyle(':')
    handles, labels = g.get_legend_handles_labels()
    handles[2].set_linestyle('--')
    handles[3].set_linestyle(':')
    # Remove legend title.
    g.legend(handles=handles[1:], labels=labels[1:])

    if output is not None:
        plt_path = os.path.join(output, f'{prefix}_{key}.pdf')
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
    ylabels = [
        'Speed ($\\frac{sites}{step}$)',  # noqa: W605
        'Throughput ($\\frac{vehicles}{step}$)',  # noqa: W605
        'Quick Decelerations ($\\frac{vehicles\%}{step}$)',  # noqa: W605
        'Lane Changes ($\\frac{vehicles\%}{step}$)',  # noqa: W605
        'Waiting Vehicles ($\\frac{vehicles\%}{step}$)'  # noqa: W605
    ]
    multipliers = [1, 1, 100, 100, 100]
    ylims = [5.5, 3.5, 6.5, 3, 60]
    for key, ylabel, multiplier, ylim in zip(keys, ylabels, multipliers, ylims):
        make_plot(df, key, ylabel, multiplier, ylim, output, prefix)


if __name__ == '__main__':
    main()
