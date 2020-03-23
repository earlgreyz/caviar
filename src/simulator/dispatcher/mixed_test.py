import unittest
from unittest.mock import Mock

from simulator.dispatcher.dispatcher import Dispatcher
from simulator.dispatcher.dispatcher_test import implementsDispatcher
from simulator.dispatcher.mixed import MixedDispatcher
from simulator.vehicle.car import CarParams


@implementsDispatcher
class MixedDispatcherTestCase(unittest.TestCase):

    def getDispatcher(self) -> Dispatcher:
        return MixedDispatcher(road=Mock(), count=1, penetration=.5, params=CarParams())


if __name__ == '__main__':
    unittest.main()
