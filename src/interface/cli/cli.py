import typing
import click
import click_config_file

from interface.cli.obstacle import ObstacleParamType, ObstacleValue, addObstacle
from interface.gui.controller import Controller

from simulator.dispatcher.car import CarDispatcher
from simulator.road.dense import DenseRoad
from simulator.road.sparse import SparseRoad
from simulator.road.speedcontroller import SpeedController
from simulator.simulator import Simulator
from simulator.vehicle.car import CarParams


@click.group()
# Road options.
@click.option('--length', default=100, help='Road length')
@click.option('--lanes', default=6, help='Number of lanes')
@click.option('--sparse', default=False, is_flag=True, help='Use sparse road implementation')
# Speed controller options.
@click.option('--max-speed', default=5, help='Road maximum speed')
@click.option('--obstacles', multiple=True, default=[], type=ObstacleParamType())
# Dispatcher options.
@click.option('--dispatch', default=2, help='Maximum number of cars dispatched each step')
@click.option('--pslow', default=.33, help='Probability a NS-model car will slow down')
@click.option('--pchange', default=.33, help='Probability a NS-model car will change a lane')
# Configuration file option.
@click_config_file.configuration_option()
@click.pass_context
def cli(ctx: click.Context, **kwargs) -> None:
    # Extract options.
    length: int = kwargs['length']
    lanes: int = kwargs['lanes']
    sparse: bool = kwargs['sparse']
    max_speed: int = kwargs['max_speed']
    dispatch: int = kwargs['dispatch']
    pslow: float = kwargs['pslow']
    pchange: float = kwargs['pchange']
    obstacles: typing.List[ObstacleValue] = kwargs['obstacles']
    # Create a road.
    speed_controller = SpeedController(max_speed=max_speed)
    if sparse:
        road = SparseRoad(length=length, lanes_count=lanes, controller=speed_controller)
    else:
        road = DenseRoad(length=length, lanes_count=lanes, controller=speed_controller)
    # Add obstacles.
    for obstacle in obstacles:
        addObstacle(road=road, obstacle=obstacle)
    # Create a dispatcher.
    car_params = CarParams(slow=pslow, change=pchange)
    dispatcher = CarDispatcher(count=dispatch, road=road, params=car_params)
    # Create a simulator.
    ctx.obj = Simulator(road=road, dispatcher=dispatcher)


@cli.command()
@click.option('--step', default=100, help='Animation time of a single simulation step (ms)')
@click.option('--fps', default=30, help='Animation frames per second')
@click.pass_context
def gui(ctx: click.Context, step: int, fps: int) -> None:
    controller = Controller(simulator=ctx.obj)
    controller.run(speed=step, refresh=fps)


@cli.command()
@click.option('--steps', default=1000, help='Number of simulation steps to run')
@click.pass_context
def simulate(ctx: click.Context, steps: int):
    simulator: Simulator = ctx.obj
    for _ in range(steps):
        simulator.step()
