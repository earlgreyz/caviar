import random

from simulator.road.road import Road
from simulator.vehicle.car import Car, CarParams


class CarDispatcher:
    count: int
    remaining: int
    road: Road

    def __init__(self, count: int, road: Road, params: CarParams):
        self.count = count
        self.remaining = 0
        self.road = road
        self.params = params

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
            car = Car(position, self.road.params.MAX_SPEED, road=self.road, params=self.params)
            self.road.addVehicle(position=position, vehicle=car)
            self.remaining -= 1
