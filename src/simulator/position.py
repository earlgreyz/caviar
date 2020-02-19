import typing

Position = typing.Tuple[int, int]


def inBounds(x: int, a: int, b: int) -> bool:
    '''
    Checks if a point is in the interval.
    :param x: point.
    :param a: lower bound (inc.)
    :param b: upper bound (exc.)
    :return: x in [a, b)
    '''
    return x >= a and x < b
