import click

from simulator.road.dense import DenseRoad
from simulator.road.road import RoadParams
from simulator.dispatcher.car import CarDispatcher
from simulator.road.sparse import SparseRoad
from simulator.simulator import Simulator
from simulator.vehicle.car import CarParams
from controller.controller import Controller


@click.command()
@click.option('--length', default=100, help='Road length')
@click.option('--lanes', default=6, help='Number of lanes')
@click.option('--speed', default=5, help='Road maximum speed')
@click.option('--sparse', default=False, is_flag=True, help='Use sparse road implementation')
@click.option('--dispatch', default=2, help='Maximum number of cars dispatched each step')
@click.option('--pslow', default=.33, help='Probability a NS-model car will slow down')
@click.option('--pchange', default=.33, help='Probability a NS-model car will change a lane')
def main(length: int, lanes: int, speed: int, sparse: bool,
         dispatch: int, pslow: float, pchange: float):
    # Create a road.
    road_params = RoadParams(speed=speed)
    if sparse:
        road = SparseRoad(length=length, lanes_count=lanes, params=road_params)
    else:
        road = DenseRoad(length=length, lanes_count=lanes, params=road_params)
    # Create a dispatcher.
    car_params = CarParams(slow=pslow, change=pchange)
    dispatcher = CarDispatcher(count=dispatch, road=road, params=car_params)
    # Create a simulator.
    simulator = Simulator(road=road, dispatcher=dispatcher)
    controller = Controller(simulator=simulator)
    # Run the simulation.
    controller.run()


if __name__ == '__main__':
    main()
