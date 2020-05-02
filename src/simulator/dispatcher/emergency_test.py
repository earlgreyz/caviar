import unittest
from unittest.mock import Mock, patch

from simulator.dispatcher.dispatcher import Dispatcher
from simulator.dispatcher.dispatcher_test import implementsDispatcher
from simulator.dispatcher.emergency import EmergencyDispatcher
from simulator.vehicle.conventional import Driver


@implementsDispatcher
class EmergencyDispatcherTestCase(unittest.TestCase):
    def getDispatcher(self) -> Dispatcher:
        return EmergencyDispatcher(
            road=Mock(), count=1, penetration=.5, driver=Driver(), frequency=20)

    def test_newEmergencyVehicle(self):
        dispatcher = EmergencyDispatcher(
            road=Mock(), count=1, penetration=.5, driver=Driver(), frequency=20)
        position = (0, 0)
        vehicle = dispatcher._newEmergencyVehicle(position=position)
        self.assertEqual(vehicle.position, position)
        self.assertTrue(vehicle.isEmergencyVehicle())

    @patch('random.randint')
    def test_dispatch(self, mocked_randint):
        road = Mock()
        road.getVehicle.return_value = None
        mocked_randint.return_value = 1
        road.lanes_count = 4
        # Test normal dispatch is called.
        dispatcher = EmergencyDispatcher(
            road=road, count=1, penetration=.5, driver=Driver(), frequency=20)
        for i in range(19):
            dispatcher.dispatch()
            road.addEmergencyVehicle.assert_not_called()
            road.addVehicle.assert_called_once()
            road.addVehicle.reset_mock()
        # Test emergency vehicle is added.
        dispatcher.dispatch()
        road.addEmergencyVehicle.assert_called_once()
        road.addVehicle.assert_called_once()
        road.addEmergencyVehicle.reset_mock()
        road.addVehicle.reset_mock()
        # Test wait for empty emergency lane to dispatch emergency.
        dispatcher.steps = 19
        road.getVehicle.return_value = Mock()
        dispatcher.dispatch()
        road.addEmergencyVehicle.assert_not_called()
        road.getVehicle.return_value = None
        dispatcher.dispatch()
        road.addEmergencyVehicle.assert_called_once()
        road.addEmergencyVehicle.reset_mock()
        road.addEmergencyVehicle.assert_not_called()


if __name__ == '__main__':
    unittest.main()
