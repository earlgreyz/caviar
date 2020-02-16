import click

from simulator.road.dense import DenseRoad
from simulator.road.road import RoadParams
from simulator.dispatcher.car import CarDispatcher
from simulator.simulator import Simulator
from simulator.vehicle.car import CarParams
from visualiser.visualiser import Visualiser


@click.command()
@click.option('--length', default=100, help='Road length')
@click.option('--lanes', default=6, help='Number of lanes')
@click.option('--speed', default=5, help='Road maximum speed')
@click.option('--dispatch', default=2, help='Maximum number of cars dispatched each step')
@click.option('--pslow', default=.33, help='Probability a NS-model car will slow down')
@click.option('--pchange', default=.33, help='Probability a NS-model car will change a lane')
def main(length: int, lanes: int, speed: int,
         dispatch: int, pslow: float, pchange: float):
    # Create a road.
    road_params = RoadParams(speed=speed)
    road = DenseRoad(length=length, lanes_count=lanes, params=road_params)
    # Create a dispatcher.
    car_params = CarParams(slow=pslow, change=pchange)
    dispatcher = CarDispatcher(count=dispatch, road=road, params=car_params)
    # Create a simulator.
    simulator = Simulator(road=road, dispatcher=dispatcher)
    visualiser = Visualiser(simulator=simulator)
    # Run the simulation.
    visualiser.run()


if __name__ == '__main__':
    main()
