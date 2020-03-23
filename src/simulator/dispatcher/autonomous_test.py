import unittest
from unittest.mock import Mock

from simulator.dispatcher.autonomous import AutonomousDispatcher
from simulator.dispatcher.dispatcher import Dispatcher
from simulator.dispatcher.dispatcher_test import implementsDispatcher


@implementsDispatcher
class AutonomousDispatcherTestCase(unittest.TestCase):
    def getDispatcher(self) -> Dispatcher:
        return AutonomousDispatcher(road=Mock(), count=1)


if __name__ == '__main__':
    unittest.main()
