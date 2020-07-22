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
    def test_dispatch__count(self, mocked_random):
        road = Mock(lanes_count=1, lane_width=1)
        road.lanes_count = 1
        road.sublanesCount = lambda _: 1
        road.canPlaceVehicle = Mock(return_value=False)
        road.getRelativePosition = lambda position: position

        # Check no vehicles added if random is zero.
        dispatcher = Dispatcher(road=road, count=1)
        vehicle = Mock()
        dispatcher._newVehicle = Mock(return_value=vehicle)
        mocked_random.return_value = 0
        dispatcher.dispatch()
        road.canPlaceVehicle.assert_not_called()
        road.addVehicle.assert_not_called()
        self.assertEqual(dispatcher.remaining, 0)

        # Check no vehicles added if all lanes are taken.
        road.reset_mock()
        mocked_random.return_value = 1
        dispatcher.dispatch()
        road.canPlaceVehicle.assert_called()
        road.addVehicle.assert_not_called()
        self.assertEqual(dispatcher.remaining, 1)

        # Check remaining vehicles are added.
        road.reset_mock()
        road.canPlaceVehicle.return_value = True
        vehicle = Mock(length=1)
        vehicle.position = (42, 42)

        def mock_newVehicle(position: Position) -> Vehicle:
            vehicle.position = position
            return vehicle

        dispatcher._newVehicle = mock_newVehicle
        mocked_random.return_value = 0
        dispatcher.dispatch()
        road.canPlaceVehicle.assert_called_with(vehicle=vehicle)
        road.addVehicle.assert_called_with(vehicle=vehicle)
        self.assertEqual(vehicle.position, (0, 0))
        self.assertEqual(dispatcher.remaining, 0)

    @patch('random.randint')
    def test_dispatch__width(self, mocked_random):
        '''
        Warning! Potentially flaky test, due to testing a random function.
        The probability the test will pass despite an error in the function is
        (2/6)**N where N is the number of times the test is repeated.
        '''
        road = Mock(lanes_count=2, lane_width=2)
        road.sublanesCount = property(lambda _: 6)
        road.canPlaceVehicle = Mock(return_value=True)

        def mock_getRelativePosition(position: Position) -> Position:
            x, lane = position
            return x, lane * 2 + 1

        road.getRelativePosition = mock_getRelativePosition

        dispatcher = Dispatcher(road=road, count=1)
        vehicle = Mock(length=1)
        vehicle.position = (42, 42)

        def mock_newVehicle(position: Position) -> Vehicle:
            vehicle.position = position
            return vehicle

        dispatcher._newVehicle = mock_newVehicle
        mocked_random.return_value = 1

        # With N=20 the probability of passing an error is lower than 1e-10.
        for _ in range(20):
            dispatcher.dispatch()
            x, lane = vehicle.position
            self.assertIn(lane, [1, 3], msg='vehicle dispatched between lanes')
            self.assertEqual(x, 0)

    @patch('random.randint')
    def test_dispatch__length(self, mocked_random):
        road = Mock(lanes_count=1, lane_width=1)
        road.canPlaceVehicle = Mock(return_value=True)
        road.getRelativePosition = lambda position: position
        mocked_random.return_value = 1
        dispatcher = Dispatcher(road=road, count=1, length=2)

        vehicle = Mock(length=2)
        vehicle.position = (42, 42)

        def mock_newVehicle(position: Position) -> Vehicle:
            vehicle.position = position
            return vehicle

        dispatcher._newVehicle = mock_newVehicle
        dispatcher.dispatch()
        road.canPlaceVehicle.assert_called_with(vehicle=vehicle)
        road.addVehicle.assert_called_with(vehicle=vehicle)
        self.assertEqual(vehicle.position, (1, 0))
        self.assertEqual(dispatcher.remaining, 0, )

        road.reset_mock()

        dispatcher = Dispatcher(road=road, count=1, length=4)
        vehicle = Mock(length=4)
        vehicle.position = (42, 42)

        def mock_newVehicle(position: Position) -> Vehicle:
            vehicle.position = position
            return vehicle

        dispatcher._newVehicle = mock_newVehicle
        dispatcher.dispatch()
        road.canPlaceVehicle.assert_called_with(vehicle=vehicle)
        road.addVehicle.assert_called_with(vehicle=vehicle)
        self.assertEqual(vehicle.position, (3, 0))
        self.assertEqual(dispatcher.remaining, 0, )


if __name__ == '__main__':
    unittest.main()
