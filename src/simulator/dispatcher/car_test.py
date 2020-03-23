import unittest
from unittest.mock import Mock

from simulator.dispatcher.car import CarDispatcher
from simulator.dispatcher.dispatcher import Dispatcher
from simulator.dispatcher.dispatcher_test import implementsDispatcher
from simulator.vehicle.car import CarParams


@implementsDispatcher
class CarDispatcherTestCase(unittest.TestCase):
    def getDispatcher(self) -> Dispatcher:
        return CarDispatcher(road=Mock(), count=1, params=CarParams())


if __name__ == '__main__':
    unittest.main()
