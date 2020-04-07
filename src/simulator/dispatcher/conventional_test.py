import unittest
from unittest.mock import Mock

from simulator.dispatcher.conventional import ConventionalDispatcher
from simulator.dispatcher.dispatcher import Dispatcher
from simulator.dispatcher.dispatcher_test import implementsDispatcher
from simulator.vehicle.conventional import Driver


@implementsDispatcher
class CarDispatcherTestCase(unittest.TestCase):
    def getDispatcher(self) -> Dispatcher:
        return ConventionalDispatcher(road=Mock(), count=1, driver=Driver())


if __name__ == '__main__':
    unittest.main()
