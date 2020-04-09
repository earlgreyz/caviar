from simulator.vehicle.autonomous import AutonomousCar


class EmergencyCar(AutonomousCar):
    def isEmergency(self) -> bool:
        return True
