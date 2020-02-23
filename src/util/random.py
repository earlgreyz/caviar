import random
import typing

T = typing.TypeVar('T')


def shuffled(xs: typing.List[T]) -> typing.List[T]:
    '''
    Creates a shuffled version of a given list.
    :param xs: list to shuffle.
    :return: shuffled list.
    '''
    return random.sample(xs, len(xs))
