import typing

Color = typing.Tuple[int, int, int]


class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARK = (67, 67, 78)
    LIGHT = (212, 212, 212)
    GREEN = (27, 176, 66)
    RED = (255, 105, 97)


def gradient(start: Color, end: Color, p: float) -> Color:
    def f(x: int, y: int, p: float) -> int:
        return round(x * (1 - p) + y * p)

    p = min(1., max(0., p))
    sr, sg, sb = start
    er, eg, eb = end
    r, g, b = f(sr, er, p), f(sg, eg, p), f(sb, eb, p)
    return (r, g, b)
