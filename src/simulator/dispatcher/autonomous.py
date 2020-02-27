import random

from simulator.dispatcher.dispatcher import Dispatcher
from simulator.road.road import Road
from simulator.vehicle.autonomous import AutonomousCar


class AutonomousDispatcher(Dispatcher):
    count: int
    remaining: int

    def __init__(self, road: Road, count: int):
        super().__init__(road=road)
        self.count = count
        self.remaining = 0

    def dispatch(self) -> None:
        self.remaining += random.randint(0, self.count)
        lanes = list(range(self.road.lanes_count))
        random.shuffle(lanes)
        for lane in lanes:
            if self.remaining <= 0:
                return
            # Check if position is not occupied.
            position = (0, lane)
            if self.road.getVehicle(position=position) is not None:
                continue
            # Place the car.
            speed = self.road.controller.getMaxSpeed(position)
            car = AutonomousCar(position, velocity=speed, road=self.road)
            self.road.addVehicle(vehicle=car)
            self.remaining -= 1
