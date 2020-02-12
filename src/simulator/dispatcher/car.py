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
            if 0 in self.road.lanes[lane]:
                return
            position = (0, lane)
            car = Car(position, self.road.params.MAX_SPEED, road=self.road, params=self.params)
            self.road.addVehicle(position=position, vehicle=car)
            self.remaining -= 1
