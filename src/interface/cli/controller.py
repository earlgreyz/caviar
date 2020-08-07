import os
import typing
import click

from charts.heatmap import HeatMap
from charts.velocity import VelocityChart

from simulator.simulator import Simulator
from simulator.statistics.averageresult import AverageResult
from simulator.statistics.collector import Collector, Statistics
from simulator.statistics.tracker import Tracker
from simulator.statistics.vehicletype import VehicleType

from util.format import OptionalFormat


class Controller:
    simulator: Simulator

    def __init__(self, simulator: Simulator):
        self.simulator = simulator

    def run(self, steps: int, skip: int, statistics: Statistics, no_charts: bool,
            output: typing.Optional[str] = None, prefix: str = '') -> None:
        with Collector(simulator=self.simulator, statistics=statistics, skip=skip) as collector, \
                Tracker(simulator=self.simulator, buffer_size=steps - skip) as tracker:

            def show_stats(_: typing.Any) -> str:
                return '{:.2f}|{:.2f}|{:.2f} (Average|Conventional|Autonomous)'.format(
                    OptionalFormat(tracker.getAverageVelocity(VehicleType.ANY)),
                    OptionalFormat(tracker.getAverageVelocity(VehicleType.CONVENTIONAL)),
                    OptionalFormat(tracker.getAverageVelocity(VehicleType.AUTONOMOUS))
                )

            with click.progressbar(range(steps), steps, item_show_func=show_stats) as bar:
                for _ in bar:
                    self.simulator.step()

            if statistics & Statistics.THROUGHPUT:
                click.secho('Generating throughput charts', fg='blue')
                throughput = HeatMap(
                    data=collector.getThrougput(), title='Throughput', max_value=3)
                if output is not None:
                    throughput.save(path=output, prefix=f'{prefix}_throughput', only_data=no_charts)
                else:
                    throughput.show(only_data=no_charts)

            if statistics & Statistics.HEAT_MAP:
                click.secho('Generating traffic density charts', fg='blue')
                heat_map = HeatMap(
                    data=collector.getHeatMap(), title='Traffic density', max_value=1)
                if output is not None:
                    heat_map.save(path=output, prefix=f'{prefix}_traffic', only_data=no_charts)
                else:
                    heat_map.show(only_data=no_charts)

            if statistics & Statistics.VELOCITY:
                click.secho('Generating speed charts', fg='blue')

                def mapper(x: AverageResult) -> float:
                    return x.toZeroFloat()

                velocity = \
                    [list(map(mapper, lane)) for lane in collector.velocity]
                autonomous = \
                    [list(map(mapper, lane)) for lane in collector.velocity_autonomous]
                conventional = \
                    [list(map(mapper, lane)) for lane in collector.velocity_conventional]
                velocity = VelocityChart(
                    car=velocity, autonomous=autonomous, conventional=conventional)
                if output is not None:
                    velocity.save(path=output, prefix=f'{prefix}_speed', only_data=no_charts)
                else:
                    velocity.show(only_data=no_charts)

            click.secho('Generating average statistics', fg='blue')
            data = tracker.getAverageData()
            if output is not None:
                data.to_csv(os.path.join(output, f'{prefix}_average.csv'), index=False)
            else:
                click.echo(data.to_csv(index=False))
