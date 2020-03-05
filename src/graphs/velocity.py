import click
import io
import yaml

import matplotlib.pyplot as plt

from graphs.command import command


@command.command()
@click.argument('file', type=click.File('rb'))
def velocity(file: io.BufferedReader):
    data = yaml.safe_load(file.read())[-100:]

    plt.style.use('ggplot')
    plt.figure()

    average = [item['average_velocity'] for item in data]
    autonomous = [item['average_velocity_autonomous'] for item in data]
    conventional = [item['average_velocity_conventional'] for item in data]

    plt.plot(average, label='Average')
    plt.plot(autonomous, label='Autonomous')
    plt.plot(conventional, label='Conventional')

    plt.ylim(bottom=0)
    plt.legend()
    plt.show()
