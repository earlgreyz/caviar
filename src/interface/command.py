import random
import typing
import click
import click_config_file
import yaml

from interface.obstacle import ObstacleParamType, ObstacleValue, addObstacle
from interface.gui.controller import Controller as GUIController
from interface.cli.controller import Controller as CLIController

from simulator.dispatcher.mixed import MixedDispatcher
from simulator.road.dense import DenseRoad
from simulator.road.speedcontroller import SpeedController
from simulator.simulator import Simulator
from simulator.statistics.collector import Statistics
from simulator.vehicle.conventional import Driver


def configProvider(file_path: str, cmd: str) -> typing.Dict[str, typing.Any]:
    print(f'Loading {file_path} of {cmd}')
    with open(file_path) as data:
        return yaml.safe_load(data)['simulation']


@click.group()
# Road options.
@click.option('--length', default=100, help='Road length')
@click.option('--width', default=1, help='Lane width')
@click.option('--lanes', default=6, help='Number of lanes')
# Speed controller options.
@click.option('--max-speed', default=5, help='Road maximum speed')
@click.option('--obstacles', multiple=True, default=[], type=ObstacleParamType())
# Dispatcher options.
@click.option('--density', default=.1, help='Initial density of vehicles on the road')
@click.option('--dispatch', default=6, help='Maximum number of cars dispatched each step')
@click.option('--penetration', default=.5, help='Penetration rate of CAV')
@click.option('--car-length', default=1, help='Number of cells occupied by a single car')
# Driver options.
@click.option('--pslow', default=.2, help='Probability a NS-model car will slow down')
@click.option('--pchange', default=.5, help='Probability a NS-model car will change a lane')
@click.option('--symmetry', default=False, is_flag=True, help='Do not use left lane to overtake')
@click.option('--limit', default=0, help='Difference in maximum speed between vehicles')
# Other options.
@click.option('--seed', type=int, help='Seed for the RNG')
# Configuration file option.
@click_config_file.configuration_option(provider=configProvider, implicit=False)
@click.pass_context
def command(ctx: click.Context, **kwargs) -> None:
    # Extract options.
    length: int = kwargs['length']
    width: int = kwargs['width']
    lanes: int = kwargs['lanes']
    max_speed: int = kwargs['max_speed']
    density: float = kwargs['density']
    dispatch: int = kwargs['dispatch']
    penetration: float = kwargs['penetration']
    car_length: int = kwargs['car_length']
    pslow: float = kwargs['pslow']
    pchange: float = kwargs['pchange']
    symmetry: bool = kwargs['symmetry']
    limit: int = kwargs['limit']
    obstacles: typing.List[ObstacleValue] = kwargs['obstacles']
    seed: typing.Optional[int] = kwargs['seed']
    # Initialize random number generator.
    if seed is not None:
        random.seed(seed)
    # Create a road.
    speed_controller = SpeedController(max_speed=max_speed)
    road = DenseRoad(
        length=length, lanes_count=lanes, lane_width=width, controller=speed_controller)
    # Add obstacles.
    for obstacle in obstacles:
        addObstacle(road=road, obstacle=obstacle)
    # Create the dispatcher.
    driver = Driver(slow=pslow, change=pchange, symmetry=symmetry)
    dispatcher = MixedDispatcher(
        count=dispatch, road=road, penetration=penetration,
        driver=driver, length=car_length, limit=limit)
    # Create the simulator and scatter vehicles.
    simulator = Simulator(road=road, dispatcher=dispatcher)
    simulator.scatterVehicles(density=density)
    ctx.obj = simulator


@command.command()
@click.option('--step', default=100, help='Animation time of a single simulation step (ms)')
@click.option('--fps', default=30, help='Animation frames per second')
@click.option('--buffer', default=1, help='Statistics buffer size')
@click.pass_context
def gui(ctx: click.Context, step: int, fps: int, buffer: int) -> None:
    controller = GUIController(simulator=ctx.obj)
    controller.run(speed=step, refresh=fps, buffer=buffer)


@command.command()
@click.option('--steps', default=1000, help='Number of simulation steps to run')
@click.option('--skip', default=0, help='Skip first n steps when gathering statistics')
@click.option('--output', '-o', type=click.Path(file_okay=False), help='Output directory')
@click.option('--prefix', '-p', default='', help='Output files name prefix')
@click.option('--no-velocity', is_flag=True, help='Do not generate velocity statistics')
@click.option('--no-traffic', is_flag=True, help='Do not generate traffic density statistics')
@click.option('--no-throughput', is_flag=True, help='Do not generate throughput statistics')
@click.pass_context
def cli(ctx: click.Context, no_velocity: bool, no_traffic: bool, no_throughput: bool, **kwargs):
    controller = CLIController(simulator=ctx.obj)
    statistics = Statistics.ALL
    if no_velocity:
        statistics &= ~statistics.VELOCITY
    if no_traffic:
        statistics &= ~statistics.HEAT_MAP
    if no_throughput:
        statistics &= ~statistics.THROUGHPUT
    controller.run(statistics=statistics, **kwargs)
