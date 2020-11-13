from simulator.dispatcher.mixed import MixedDispatcher
from simulator.road.road import Road
from simulator.vehicle.conventional import Driver
from simulator.vehicle.emergency import EmergencyCar


class EmergencyDispatcher(MixedDispatcher):
    emergency_rate: int
    emergency: bool

    def __init__(self, road: Road, count: int, penetration: float, driver: Driver,
                 emergency_rate: int, length: int = 1, limit: int = 0):
        super().__init__(road=road, count=count, length=length, penetration=penetration,
                         driver=driver, limit=limit)
        self.emergency_rate = emergency_rate
        self.emergency = False

    def dispatch(self, step: int) -> None:
        if self.emergency_rate > 0 and step % self.emergency_rate == 0:
            self.emergency = True

        if self.emergency:
            position = (self.length - 1, self.road.emergencyLane)
            speed = self.road.controller.getMaxSpeed(position, width=self.road.lane_width)
            vehicle = EmergencyCar(position=position, velocity=speed, road=self.road,
                                   length=self.length, width=self.road.lane_width)
            # Add the vehicle if possible.
            if self.road.canPlaceVehicle(vehicle=vehicle):
                self.road.addEmergencyVehicle(vehicle=vehicle)
                self.emergency = False

        # Dispatch other vehicles.
        super().dispatch(step=step)
