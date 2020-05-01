from simulator.dispatcher.mixed import MixedDispatcher
from simulator.position import Position
from simulator.road.road import Road
from simulator.vehicle.conventional import Driver
from simulator.vehicle.emergency import EmergencyCar
from simulator.vehicle.vehicle import Vehicle


class EmergencyDispatcher(MixedDispatcher):
    frequency: int
    steps: int

    def __init__(self, road: Road, count: int, penetration: float, driver: Driver,
                 frequency: int = 0, length: int = 1, limit: int = 0):
        super().__init__(road=road, count=count, penetration=penetration, driver=driver,
                         length=length, limit=limit)
        self.steps = 0
        self.frequency = frequency

    def dispatch(self) -> None:
        if self.frequency > 0:
            self.steps = (self.steps + 1) % self.frequency
            if self.steps == 0:
                position = (self.length - 1, Road.EMERGENCY_LANE)
                if self.road.getVehicle(position=position) is None:
                    self.road.addEmergencyVehicle(self._newEmergencyVehicle(position=position))
                else:
                    self.steps -= 1  # Try to dispatch in the next step.
        super().dispatch()

    def _newEmergencyVehicle(self, position: Position) -> Vehicle:
        speed = self.road.controller.getMaxSpeed(position)
        return EmergencyCar(position=position, velocity=speed, road=self.road, length=self.length)
