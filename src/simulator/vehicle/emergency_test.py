import unittest
from unittest.mock import Mock

from simulator.vehicle.emergency import EmergencyCar


class EmergencyCarTestCase(unittest.TestCase):
    def test_isEmergency(self):
        car = EmergencyCar(position=(0, 0), velocity=1, road=Mock())
        self.assertTrue(car.isEmergencyVehicle())


if __name__ == '__main__':
    unittest.main()
