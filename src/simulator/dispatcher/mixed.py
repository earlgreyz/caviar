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

    def __init__(self, road: Road, count: int, penetration: float, driver: Driver,
                 length: int = 1):
        super().__init__(road=road, count=count, length=length)
        self.penetration = penetration
        self.driver = driver

    def _newVehicle(self, position: Position) -> Vehicle:
        speed = self.road.controller.getMaxSpeed(position)
        params = dict(position=position, velocity=speed, road=self.road, length=self.length)
        if random.random() < self.penetration:
            return AutonomousCar(**params)
        else:
            return ConventionalCar(**params, driver=self.driver)
