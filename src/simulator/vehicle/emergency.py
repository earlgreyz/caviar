from simulator.vehicle.autonomous import AutonomousCar


class EmergencyCar(AutonomousCar):
    def isEmergencyVehicle(self) -> bool:
        return True
