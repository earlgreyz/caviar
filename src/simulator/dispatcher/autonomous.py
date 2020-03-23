from simulator.dispatcher.dispatcher import Dispatcher
from simulator.position import Position
from simulator.vehicle.autonomous import AutonomousCar
from simulator.vehicle.vehicle import Vehicle


class AutonomousDispatcher(Dispatcher):
    def _newVehicle(self, position: Position) -> Vehicle:
        speed = self.road.controller.getMaxSpeed(position)
        return AutonomousCar(position, velocity=speed, road=self.road)
