import unittest
from unittest.mock import Mock, patch

from simulator.dispatcher.dispatcher import Dispatcher
from simulator.position import Position
from simulator.vehicle.vehicle import Vehicle


def implementsDispatcher(cls):
    assert hasattr(cls, 'getDispatcher') and callable(getattr(cls, 'getDispatcher'))

    def test_implementsDispatcher(self: cls):
        dispatcher: Dispatcher = self.getDispatcher()
        position = (42, 0)
        vehicle = dispatcher._newVehicle(position=position)
        self.assertEqual(vehicle.position, position, 'invalid vehicle position')

    cls.test_implementsDispatcher = test_implementsDispatcher
    return cls


class DispatcherTestCase(unittest.TestCase):
    def test_interface(self):
        dispatcher = Dispatcher(road=Mock(), count=1)
        with self.assertRaises(NotImplementedError, msg='expected _newVehicle to be virtual'):
            dispatcher._newVehicle(position=(0, 0))

    @patch('random.randint')
    def test_dispatch(self, mocked_random):
        road = Mock()
        road.lanes_count = 1

        # Check no vehicles added if random is zero.
        dispatcher = Dispatcher(road=road, count=1)
        mocked_random.return_value = 0
        dispatcher.dispatch()
        road.addVehicle.assert_not_called()
        self.assertEqual(dispatcher.remaining, 0, 'expected no remaining vehicles')

        # Check no vehicles added if all lanes are taken.
        road.reset_mock()
        road.getVehicle.return_value = Mock()
        mocked_random.return_value = 1
        dispatcher.dispatch()
        road.addVehicle.assert_not_called()
        self.assertEqual(dispatcher.remaining, 1, 'expected one remaining vehicle')

        # Check remaining vehicles are added.
        road.reset_mock()
        vehicle = Mock()
        vehicle.position = (42, 42)

        def mock_newVehicle(position: Position) -> Vehicle:
            vehicle.position = position
            return vehicle

        dispatcher._newVehicle = mock_newVehicle
        road.getVehicle.return_value = None
        mocked_random.return_value = 0
        dispatcher.dispatch()
        road.getVehicle.assert_called()
        road.addVehicle.assert_called_with(vehicle=vehicle)
        self.assertEqual(vehicle.position, (0, 0), 'expected vehicle position to be (0, 0)')
        self.assertEqual(dispatcher.remaining, 0, 'expected no remaining vehicles')

    @patch('random.randint')
    def test_dispatch_long(self, mocked_random):
        road = Mock()
        road.lanes_count = 1
        mocked_random.return_value = 1
        dispatcher = Dispatcher(road=road, count=1, length=2)

        vehicle = Mock(length=2)
        vehicle.position = (42, 42)

        def mock_newVehicle(position: Position) -> Vehicle:
            vehicle.position = position
            return vehicle

        dispatcher._newVehicle = mock_newVehicle
        road.getVehicle.return_value = None
        dispatcher.dispatch()
        road.getVehicle.assert_called()
        road.addVehicle.assert_called_with(vehicle=vehicle)
        self.assertEqual(vehicle.position, (1, 0), 'expected vehicle position to be (2, 0)')
        self.assertEqual(dispatcher.remaining, 0, 'expected no remaining vehicles')


if __name__ == '__main__':
    unittest.main()
