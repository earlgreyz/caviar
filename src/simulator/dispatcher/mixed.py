import random

from simulator.dispatcher.dispatcher import Dispatcher
from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.car import Car, CarParams
from simulator.vehicle.autonomous import AutonomousCar
from simulator.vehicle.vehicle import Vehicle


class MixedDispatcher(Dispatcher):
    penetration: float
    params: CarParams

    def __init__(self, road: Road, count: int, penetration: float, params: CarParams):
        super().__init__(road=road, count=count)
        self.penetration = penetration
        self.params = params

    def _newVehicle(self, position: Position) -> Vehicle:
        speed = self.road.controller.getMaxSpeed(position)
        if random.random() < self.penetration:
            return AutonomousCar(position, velocity=speed, road=self.road)
        else:
            return Car(position, velocity=speed, road=self.road, params=self.params)
