from simulator.dispatcher.dispatcher import Dispatcher
from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.conventional import ConventionalCar, Driver
from simulator.vehicle.vehicle import Vehicle


class ConventionalDispatcher(Dispatcher):
    driver: Driver

    def __init__(self, road: Road, count: int, driver: Driver):
        super().__init__(road=road, count=count)
        self.driver = driver

    def _newVehicle(self, position: Position) -> Vehicle:
        speed = self.road.controller.getMaxSpeed(position)
        return ConventionalCar(
            position=position, velocity=speed, road=self.road,
            length=self.length, width=self.road.lane_width, driver=self.driver)
