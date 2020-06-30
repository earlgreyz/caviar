import random

from simulator.dispatcher.dispatcher import Dispatcher
from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.conventional import ConventionalCar, Driver
from simulator.vehicle.autonomous import AutonomousCar
from simulator.vehicle.vehicle import Vehicle


class MixedDispatcher(Dispatcher):
    penetration: float
    driver: Driver
    limit: int

    def __init__(self, road: Road, count: int, penetration: float, driver: Driver,
                 length: int = 1, limit: int = 0):
        super().__init__(road=road, count=count, length=length)
        self.penetration = penetration
        self.driver = driver
        self.limit = limit

    def _newVehicle(self, position: Position) -> Vehicle:
        limit = random.randint(-self.limit, self.limit)
        speed = self.road.controller.getMaxSpeed(position) + limit
        params = dict(
            position=position, velocity=speed, road=self.road, length=self.length, limit=limit)
        if random.random() < self.penetration:
            return AutonomousCar(**params)
        else:
            return ConventionalCar(**params, driver=self.driver)
