import click
import click_config_file

from simulator.dispatcher.car import CarDispatcher
from simulator.road.dense import DenseRoad
from simulator.road.sparse import SparseRoad
from simulator.road.speedcontroller import SpeedController
from simulator.simulator import Simulator
from simulator.vehicle.car import CarParams
from interface.controller import Controller


@click.command()
# Road options.
@click.option('--length', default=100, help='Road length')
@click.option('--lanes', default=6, help='Number of lanes')
@click.option('--sparse', default=False, is_flag=True, help='Use sparse road implementation')
# Speed controller options.
@click.option('--max-speed', default=5, help='Road maximum speed')
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

    # Create a road.
    speed_controller = SpeedController(max_speed=max_speed)
    if sparse:
        road = SparseRoad(length=length, lanes_count=lanes, controller=speed_controller)
    else:
        road = DenseRoad(length=length, lanes_count=lanes, controller=speed_controller)
    # Create a dispatcher.
    car_params = CarParams(slow=pslow, change=pchange)
    dispatcher = CarDispatcher(count=dispatch, road=road, params=car_params)
    # Create a simulator.
    simulator = Simulator(road=road, dispatcher=dispatcher)
    controller = Controller(simulator=simulator)
    # Run the simulation.
    controller.run()
