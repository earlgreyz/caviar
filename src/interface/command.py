import random
import typing
import click
import click_config_file
import yaml

from interface.obstacle import ObstacleParamType, ObstacleValue, addObstacle
from interface.gui.controller import Controller as GUIController
from interface.cli.controller import Controller as CLIController

from simulator.dispatcher.emergency import EmergencyDispatcher
from simulator.road.dense import DenseRoad
from simulator.road.speedcontroller import SpeedController
from simulator.simulator import Simulator
from simulator.vehicle.conventional import Driver


def configProvider(file_path: str, cmd: str) -> typing.Dict[str, typing.Any]:
    print(f'Loading {file_path} of {cmd}')
    with open(file_path) as data:
        return yaml.safe_load(data)['simulation']


@click.group()
# Road options.
@click.option('--length', default=100, help='Road length')
@click.option('--lanes', default=6, help='Number of lanes')
# Speed controller options.
@click.option('--max-speed', default=5, help='Road maximum speed')
@click.option('--obstacles', multiple=True, default=[], type=ObstacleParamType())
# Dispatcher options.
@click.option('--dispatch', default=6, help='Maximum number of cars dispatched each step')
@click.option('--penetration', default=.5, help='Penetration rate of CAV')
@click.option('--car-length', default=1, help='Number of cells occupied by a single car')
# Driver options.
@click.option('--pslow', default=.2, help='Probability a NS-model car will slow down')
@click.option('--pchange', default=.5, help='Probability a NS-model car will change a lane')
@click.option('--symmetry', default=False, is_flag=True, help='Do not use left lane to overtake')
@click.option('--limit', default=0, help='Difference in maximum speed between vehicles')
# Other options.
@click.option('--emergency', default=0, help='Dispatch an emergency vehicle every N steps')
@click.option('--seed', type=int, help='Seed for the RNG')
@click.option('--buffer', default=10, help='Number of steps in moving average calculation')
# Configuration file option.
@click_config_file.configuration_option(provider=configProvider, implicit=False)
@click.pass_context
def command(ctx: click.Context, **kwargs) -> None:
    # Extract options.
    length: int = kwargs['length']
    lanes: int = kwargs['lanes']
    max_speed: int = kwargs['max_speed']
    dispatch: int = kwargs['dispatch']
    penetration: float = kwargs['penetration']
    car_length: int = kwargs['car_length']
    pslow: float = kwargs['pslow']
    pchange: float = kwargs['pchange']
    symmetry: bool = kwargs['symmetry']
    limit: int = kwargs['limit']
    emergency: int = kwargs['emergency']
    obstacles: typing.List[ObstacleValue] = kwargs['obstacles']
    seed: typing.Optional[int] = kwargs['seed']
    buffer: int = kwargs['buffer']
    # Initialize random number generator.
    if seed is not None:
        random.seed(seed)
    # Create a road.
    speed_controller = SpeedController(max_speed=max_speed)
    road = DenseRoad(length=length, lanes_count=lanes, controller=speed_controller)
    # Add obstacles.
    for obstacle in obstacles:
        addObstacle(road=road, obstacle=obstacle)
    # Create a dispatcher.
    driver = Driver(slow=pslow, change=pchange, symmetry=symmetry)
    driver = Driver(slow=pslow, change=pchange)
    dispatcher = EmergencyDispatcher(
        count=dispatch, road=road, penetration=penetration,
        driver=driver, length=car_length, limit=limit,
        frequency=emergency)
    # Create a simulator.
    ctx.obj = Simulator(road=road, dispatcher=dispatcher, buffer_size=buffer)


@command.command()
@click.option('--step', default=100, help='Animation time of a single simulation step (ms)')
@click.option('--fps', default=30, help='Animation frames per second')
@click.pass_context
def gui(ctx: click.Context, step: int, fps: int) -> None:
    controller = GUIController(simulator=ctx.obj)
    controller.run(speed=step, refresh=fps)


@command.command()
@click.option('--steps', default=1000, help='Number of simulation steps to run')
@click.option('--individual', default=False, is_flag=True, help='Show individual statistics')
@click.option('--final', default=False, is_flag=True, help='Show only final statistics')
@click.pass_context
def cli(ctx: click.Context, steps: int, individual: bool, final: bool):
    controller = CLIController(simulator=ctx.obj)
    controller.run(steps=steps, individual=individual, final=final)
