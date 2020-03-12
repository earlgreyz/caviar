import random

from simulator.dispatcher.dispatcher import Dispatcher
from simulator.road.road import Road
from simulator.vehicle.car import Car, CarParams
from util.rand import shuffled


class CarDispatcher(Dispatcher):
    count: int
    remaining: int
    params: CarParams

    def __init__(self, road: Road, count: int, params: CarParams):
        super().__init__(road=road)
        self.count = count
        self.remaining = 0
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
            car = Car(position, velocity=speed, road=self.road, params=self.params)
            self.road.addVehicle(vehicle=car)
            self.remaining -= 1
