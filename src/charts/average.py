import os

import click
import typing

import pandas as pd


@click.command()
@click.option('--output', '-o', default=None, help='Save output to a directory')
@click.option('--prefix', '-p', default='', help='Prefix for output file names')
@click.argument('files', nargs=-1, type=click.File())
def main(output: typing.Optional[str], prefix: str, files):
    data = None
    if len(files) < 1:
        click.secho('Requires at least one data file', fg='red')
        exit(1)

    for file in files:
        current = pd.read_csv(file, header=0, index_col=0)
        if data is not None:
            data += current
        else:
            data = current

    data /= len(files)
    if output is not None:
        csv_path = os.path.join(output, f'{prefix}_average.csv')
        data.to_csv(csv_path)
    else:
        print(data.to_csv())


if __name__ == '__main__':
    main()
