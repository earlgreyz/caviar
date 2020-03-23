import unittest
from unittest.mock import Mock

from simulator.dispatcher.dispatcher import Dispatcher


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


if __name__ == '__main__':
    unittest.main()
