import os

import click
import typing

import pandas as pd


@click.command()
@click.option('--output', '-o', default=None, help='Save output to a directory')
@click.option('--prefix', '-p', default='', help='Prefix for output file names')
@click.option('-x', type=int, help='append x column value')
@click.argument('files', nargs=-1, type=click.File())
def main(output: typing.Optional[str], prefix: str, x: typing.Optional[int], files):
    df = None
    if len(files) < 1:
        click.secho('Requires at least one data file', fg='red')
        exit(1)

    for file in files:
        current = pd.read_csv(file, header=0)
        df = df.append(current) if df is not None else current

    if x is not None:
        df.insert(0, 'x', x)

    if output is not None:
        csv_path = os.path.join(output, f'{prefix}.csv')
        df.to_csv(csv_path, index=False)
    else:
        print(df.to_csv(index=False))


if __name__ == '__main__':
    main()
