import random

from simulator.dispatcher.dispatcher import Dispatcher
from simulator.road.road import Road
from simulator.vehicle.car import Car, CarParams
from simulator.vehicle.autonomous import AutonomousCar
from util.rand import shuffled


class MixedDispatcher(Dispatcher):
    count: int
    remaining: int
    penetration: float
    params: CarParams

    def __init__(self, road: Road, count: int, penetration: float, params: CarParams):
        super().__init__(road=road)
        self.count = count
        self.remaining = 0
        self.penetration = penetration
        self.params = params

    def dispatch(self) -> None:
        self.remaining += random.randint(0, self.count)
        for lane in shuffled(range(self.road.lanes_count)):
            if self.remaining <= 0:
                return
            # Check if position is not occupied.
            position = (0, lane)
            if self.road.getVehicle(position=position) is not None:
                continue
            # Place the car.
            speed = self.road.controller.getMaxSpeed(position)
            if random.random() <= self.penetration:
                car = AutonomousCar(position, velocity=speed, road=self.road)
            else:
                car = Car(position, velocity=speed, road=self.road, params=self.params)
            self.road.addVehicle(vehicle=car)
            self.remaining -= 1
