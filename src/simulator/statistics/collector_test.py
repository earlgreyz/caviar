import unittest
from unittest.mock import Mock

from simulator.statistics.collector import Collector, Statistics


class CollectorTestCase(unittest.TestCase):
    def test_init(self):
        simulator = Mock()
        simulator.road = Mock(length=100, lanes_count=1)
        collector = Collector(simulator=simulator)
        self.assertEqual(collector.statistics, Statistics.ALL)
        self.assertIsNotNone(collector.velocity)
        self.assertIsNotNone(collector.velocity_autonomous)
        self.assertIsNotNone(collector.velocity_conventional)
        self.assertIsNotNone(collector.throughput)
        self.assertIsNotNone(collector.heat_map)
        collector = Collector(simulator=simulator, statistics=Statistics.VELOCITY)
        self.assertEqual(collector.statistics, Statistics.VELOCITY)
        self.assertIsNotNone(collector.velocity)
        self.assertIsNotNone(collector.velocity_autonomous)
        self.assertIsNotNone(collector.velocity_conventional)
        self.assertFalse(hasattr(collector, 'throughput'))
        self.assertFalse(hasattr(collector, 'heat_map'))
        collector = Collector(simulator=simulator, statistics=Statistics.THROUGHPUT)
        self.assertEqual(collector.statistics, Statistics.THROUGHPUT)
        self.assertFalse(hasattr(collector, 'velocity'))
        self.assertFalse(hasattr(collector, 'velocity_autonomous'))
        self.assertFalse(hasattr(collector, 'velocity_conventional'))
        self.assertIsNotNone(collector.throughput)
        self.assertFalse(hasattr(collector, 'heat_map'))
        collector = Collector(simulator=simulator, statistics=Statistics.HEAT_MAP)
        self.assertEqual(collector.statistics, Statistics.HEAT_MAP)
        self.assertFalse(hasattr(collector, 'velocity'))
        self.assertFalse(hasattr(collector, 'velocity_autonomous'))
        self.assertFalse(hasattr(collector, 'velocity_conventional'))
        self.assertFalse(hasattr(collector, 'throughput'))
        self.assertIsNotNone(collector.heat_map)

    def test_run(self):
        simulator = Mock()
        simulator.road = Mock(length=100, lanes_count=1)

        def mock_collect(collector: Collector) -> Collector:
            collector._collectVelocity = Mock()
            collector._collectThroughput = Mock()
            collector._collectHeatMap = Mock()
            return collector

        def collect_mock_reset(collector: Collector) -> None:
            collector._collectThroughput.reset_mock()
            collector._collectVelocity.reset_mock()
            collector._collectHeatMap.reset_mock()

        # Test all statistics.
        collector = mock_collect(Collector(simulator=simulator))
        for i in range(1, 100):
            collect_mock_reset(collector)
            collector.run()
            self.assertEqual(i, collector.steps)
            collector._collectVelocity.assert_called_once()
            collector._collectThroughput.assert_called_once()
            collector._collectHeatMap.assert_called_once()
        # Test skip.
        collector = mock_collect(Collector(simulator=simulator, skip=10))
        for i in range(1, 11):
            collect_mock_reset(collector)
            collector.run()
            self.assertEqual(i, collector.steps)
            collector._collectVelocity.assert_not_called()
            collector._collectThroughput.assert_not_called()
            collector._collectHeatMap.assert_not_called()
        for i in range(11, 100):
            collect_mock_reset(collector)
            collector.run()
            self.assertEqual(i, collector.steps)
            collector._collectVelocity.assert_called_once()
            collector._collectThroughput.assert_called_once()
            collector._collectHeatMap.assert_called_once()
        # Test individual statisrics not gathered.
        collector = mock_collect(Collector(simulator=simulator, statistics=Statistics.VELOCITY))
        for i in range(1, 100):
            collect_mock_reset(collector)
            collector.run()
            self.assertEqual(i, collector.steps)
            collector._collectVelocity.assert_called_once()
            collector._collectThroughput.assert_not_called()
            collector._collectHeatMap.assert_not_called()
        collector = mock_collect(Collector(simulator=simulator, statistics=Statistics.THROUGHPUT))
        for i in range(1, 100):
            collect_mock_reset(collector)
            collector.run()
            self.assertEqual(i, collector.steps)
            collector._collectVelocity.assert_not_called()
            collector._collectThroughput.assert_called_once()
            collector._collectHeatMap.assert_not_called()
        collector = mock_collect(Collector(simulator=simulator, statistics=Statistics.HEAT_MAP))
        for i in range(1, 100):
            collect_mock_reset(collector)
            collector.run()
            self.assertEqual(i, collector.steps)
            collector._collectVelocity.assert_not_called()
            collector._collectThroughput.assert_not_called()
            collector._collectHeatMap.assert_called_once()

    def test_road(self):
        road = Mock()
        simulator = Mock(road=road)
        collector = Collector(simulator=simulator, statistics=Statistics.NONE)
        self.assertIs(road, collector._road)


if __name__ == '__main__':
    unittest.main()
