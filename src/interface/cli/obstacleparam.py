import click
import typing

ObstacleValue = typing.Tuple[int, int, int]


class ObstacleParamType(click.ParamType):
    name = 'obstacle'

    def convert(self, value: str, param: click.Parameter, ctx: click.Context) -> ObstacleValue:
        tmp = value.split(':')
        if len(tmp) != 2:
            self._invalidFormat(value, param, ctx)
        lane, tmp = tmp
        tmp = tmp.split('-')
        if len(tmp) != 2:
            self._invalidFormat(value, param, ctx)
        begin, end = tmp
        try:
            return int(lane), int(begin), int(end)
        except ValueError:
            self.fail(
                f'expected valid integers, got LANE="{lane}", BEGIN="{begin}", END="{end}"',
                param,
                ctx,
            )

    def _invalidFormat(self, value: str, param: click.Parameter, ctx: click.Context) -> None:
        self.fail(
            f'expected obstacle to be of format LANE:BEGIN-END, got "{value}" instead',
            param,
            ctx,
        )
