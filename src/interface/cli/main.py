import typing
import click
import click_config_file

from interface.cli.obstacleparam import ObstacleParamType, ObstacleValue
from interface.gui.controller import Controller

from simulator.dispatcher.car import CarDispatcher
from simulator.position import inBounds
from simulator.road.dense import DenseRoad
from simulator.road.road import Road
from simulator.road.sparse import SparseRoad
from simulator.road.speedcontroller import SpeedController
from simulator.simulator import Simulator
from simulator.vehicle.car import CarParams
from simulator.vehicle.obstacle import Obstacle


def _addObstacle(road: Road, obstacle: ObstacleValue) -> None:
    lane, begin, end = obstacle
    if not inBounds(lane, 0, road.lanes_count):
        raise ValueError(f'invalid obstacle, lane {lane} is not on the road')
    if not inBounds(begin, 0, road.length) or not inBounds(end, 0, road.length):
        raise ValueError(f'invalid obstacle, position {(begin, end)} is not on the road')
    for x in range(begin, end + 1):
        road.addVehicle(Obstacle(position=(x, lane)))


@click.command()
# Road options.
@click.option('--length', default=100, help='Road length')
@click.option('--lanes', default=6, help='Number of lanes')
@click.option('--sparse', default=False, is_flag=True, help='Use sparse road implementation')
# Speed controller options.
@click.option('--max-speed', default=5, help='Road maximum speed')
@click.option('--obstacle', multiple=True, default=[], type=ObstacleParamType())
# Dispatcher options.
@click.option('--dispatch', default=2, help='Maximum number of cars dispatched each step')
@click.option('--pslow', default=.33, help='Probability a NS-model car will slow down')
@click.option('--pchange', default=.33, help='Probability a NS-model car will change a lane')
# Configuration file option.
@click_config_file.configuration_option()
def main(**kwargs):
    # Extract options
    length: int = kwargs['length']
    lanes: int = kwargs['lanes']
    sparse: bool = kwargs['sparse']
    max_speed: int = kwargs['max_speed']
    dispatch: int = kwargs['dispatch']
    pslow: float = kwargs['pslow']
    pchange: float = kwargs['pchange']
    obstacles: typing.List[ObstacleValue] = kwargs['obstacle']

    # Create a road.
    speed_controller = SpeedController(max_speed=max_speed)
    if sparse:
        road = SparseRoad(length=length, lanes_count=lanes, controller=speed_controller)
    else:
        road = DenseRoad(length=length, lanes_count=lanes, controller=speed_controller)
    # Add obstacles.
    for obstacle in obstacles:
        _addObstacle(road=road, obstacle=obstacle)
    # Create a dispatcher.
    car_params = CarParams(slow=pslow, change=pchange)
    dispatcher = CarDispatcher(count=dispatch, road=road, params=car_params)
    # Create a simulator.
    simulator = Simulator(road=road, dispatcher=dispatcher)
    controller = Controller(simulator=simulator)
    # Run the simulation.
    controller.run()
