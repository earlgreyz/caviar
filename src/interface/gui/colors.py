import typing

Color = typing.Tuple[int, int, int]


class Colors:
    WHITE = (255, 255, 255)
    BLACK = (232, 168, 32)
    DARK = (67, 67, 78)
    LIGHT = (255, 255, 255)
    GREEN = (246, 104, 185)
    RED = (34, 193, 248)
    PURPLE = (155, 104, 237)
    BLUE = (0, 195, 177)


def gradient(start: Color, end: Color, p: float) -> Color:
    def f(x: int, y: int, p: float) -> int:
        return round(x * (1 - p) + y * p)

    p = min(1., max(0., p))
    sr, sg, sb = start
    er, eg, eb = end
    r, g, b = f(sr, er, p), f(sg, eg, p), f(sb, eb, p)
    return (r, g, b)
