import unittest
from unittest.mock import Mock, patch

from simulator.dispatcher.dispatcher import Dispatcher
from simulator.dispatcher.dispatcher_test import implementsDispatcher
from simulator.dispatcher.mixed import MixedDispatcher
from simulator.vehicle.autonomous import AutonomousCar
from simulator.vehicle.car import CarParams, Car


@implementsDispatcher
class MixedDispatcherTestCase(unittest.TestCase):
    def getDispatcher(self) -> Dispatcher:
        return MixedDispatcher(road=Mock(), count=1, penetration=.5, params=CarParams())

    @patch('random.random')
    def test_penetrationRate(self, mocked_random):
        # Penetration rate 50%.
        dispatcher = MixedDispatcher(road=Mock(), count=1, penetration=.5, params=CarParams())
        mocked_random.return_value = 0
        vehicle = dispatcher._newVehicle(position=(42, 0))
        self.assertIsInstance(vehicle, AutonomousCar, 'expected AutonomousCar')
        mocked_random.return_value = .49
        vehicle = dispatcher._newVehicle(position=(42, 0))
        self.assertIsInstance(vehicle, AutonomousCar, 'expected AutonomousCar')
        mocked_random.return_value = .5
        vehicle = dispatcher._newVehicle(position=(42, 0))
        self.assertIsInstance(vehicle, Car, 'expected Car')
        mocked_random.return_value = .99
        vehicle = dispatcher._newVehicle(position=(42, 0))
        self.assertIsInstance(vehicle, Car, 'expected Car')
        # Penetration rate 0%.
        dispatcher = MixedDispatcher(road=Mock(), count=1, penetration=0, params=CarParams())
        mocked_random.return_value = 0
        vehicle = dispatcher._newVehicle(position=(42, 0))
        self.assertIsInstance(vehicle, Car, 'expected Car')
        mocked_random.return_value = .99
        vehicle = dispatcher._newVehicle(position=(42, 0))
        self.assertIsInstance(vehicle, Car, 'expected Car')
        # Penetration rate 100%.
        dispatcher = MixedDispatcher(road=Mock(), count=1, penetration=1, params=CarParams())
        mocked_random.return_value = 0
        vehicle = dispatcher._newVehicle(position=(42, 0))
        self.assertIsInstance(vehicle, AutonomousCar, 'expected AutonomousCar')
        mocked_random.return_value = .99
        vehicle = dispatcher._newVehicle(position=(42, 0))
        self.assertIsInstance(vehicle, AutonomousCar, 'expected AutonomousCar')


if __name__ == '__main__':
    unittest.main()
