import unittest
from unittest.mock import Mock, patch

from simulator.position import Position
from simulator.simulator import Simulator, Hook
from simulator.vehicle.vehicle import Vehicle


class SimulatorTestCase(unittest.TestCase):
    @patch('random.random')
    def test_scatterVehicles(self, patched_random):
        road = Mock(length=10, lanes_count=1)

        def mock_getRelativePosition(position: Position) -> Position:
            return position

        road.getRelativePosition.side_effect = mock_getRelativePosition
        dispatcher = Mock()

        def mock_newVehicle(position: Position) -> Vehicle:
            return Mock(position=position)

        dispatcher._newVehicle.side_effect = mock_newVehicle
        simulator = Simulator(road=road, dispatcher=dispatcher)
        # Road fully occupied.
        road.canPlaceVehicle.return_value = False
        simulator.scatterVehicles(1.0)
        road.addVehicle.assert_not_called()
        # Low density.
        road.canPlaceVehicle.return_value = True
        patched_random.return_value = 1
        simulator.scatterVehicles(0)
        road.addVehicle.assert_not_called()
        # Add a vehicle.
        road.canPlaceVehicle.side_effect = [True, True] + [False] * 8
        patched_random.side_effect = [0, 1, 0]
        simulator.scatterVehicles(.5)
        road.addVehicle.assert_called_once()

    def test_step(self):
        road = Mock()
        dispatcher = Mock()
        simulator = Simulator(road=road, dispatcher=dispatcher)
        # No hooks.
        simulator.step()
        self.assertEqual(simulator.steps, 1)
        dispatcher.dispatch.assert_called_once()
        road.step.assert_called_once()
        # Test hooks are run.
        hook = Mock()
        simulator.addHook(hook)
        simulator.step()
        self.assertEqual(simulator.steps, 2)
        hook.run.assert_called_once()
        # Tests hooks are removed correctly.
        hook.run.reset_mock()
        simulator.removeHook(hook)
        simulator.step()
        self.assertEqual(simulator.steps, 3)
        hook.run.assert_not_called()

    def test_addHook(self):
        simulator = Simulator(road=Mock(), dispatcher=Mock())
        hook = Mock()
        simulator.addHook(hook)
        self.assertIn(hook, simulator.hooks)
        simulator.removeHook(hook)
        self.assertNotIn(hook, simulator.hooks)


class HookTestCase(unittest.TestCase):
    def test_interface(self):
        hook = Hook(simulator=Mock())
        with self.assertRaises(NotImplementedError):
            hook.run()

    def test_context(self):
        simulator = Mock()
        hook = Hook(simulator=simulator)
        with hook:
            simulator.addHook.assert_called_once_with(hook)
            simulator.removeHook.assert_not_called()
        simulator.removeHook.assert_called_once_with(hook)


if __name__ == '__main__':
    unittest.main()
