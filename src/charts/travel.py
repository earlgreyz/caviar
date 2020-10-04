import os

import click
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import typing


class TravelHistogram:
    data: pd.DataFrame

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def _prepareChart(self):
        # Do not use LaTeX if NO_LATEX variable is set.
        no_latex = bool(os.getenv('NO_LATEX', False))
        params = dict(font='serif', style='white')
        if not no_latex:
            params['rc'] = {'text.usetex': True}
        sns.set(**params)

        f = plt.figure(figsize=(6, 4))
        f.tight_layout()
        g = sns.lineplot(x='x', y='y', hue='type', data=self.data)
        if not no_latex:
            ylabel = 'Vehicles (\%)'  # noqa: W605
        else:
            ylabel = 'Vehicles (%)'
        g.set(xlabel='Steps', ylabel=ylabel)
        handles, labels = g.get_legend_handles_labels()
        # Remove legend title.
        g.legend(handles=handles[1:], labels=labels[1:])

    def show(self, only_data: bool = False) -> None:
        print(self.data.to_csv())
        if not only_data:
            self._prepareChart()
            plt.show()

    def save(self, path: str, prefix: str, only_data: bool) -> None:
        csv_path = os.path.join(path, f'{prefix}_travel.csv')
        self.data.to_csv(csv_path)
        if not only_data:
            self._prepareChart()
            plt_path = os.path.join(path, f'{prefix}_travel.pdf')
            plt.savefig(plt_path, bbox_inches='tight')


@click.command()
@click.option('--output', '-o', default=None, help='Save output to a directory')
@click.option('--prefix', '-p', default='', help='Prefix for output file names')
@click.argument('files', nargs=-1, type=click.File())
def main(output: typing.Optional[str], prefix: str, files):
    df = None
    if len(files) < 1:
        click.secho('Requires at least one data file', fg='red')
        exit(1)

    for file in files:
        current = pd.read_csv(file, header=0)
        df = df.append(current) if df is not None else current

    travel = TravelHistogram(data=df)
    if output is not None:
        travel.save(output, prefix, only_data=False)
    else:
        travel.show(only_data=False)


if __name__ == '__main__':
    main()
