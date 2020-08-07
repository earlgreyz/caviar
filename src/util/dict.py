import typing
from collections import OrderedDict

K = typing.TypeVar('K')
V = typing.TypeVar('V')


def makeOrderedDict(unordered: typing.Dict[K, V], order: typing.Iterable[K]) \
        -> typing.OrderedDict[K, V]:
    result = OrderedDict()
    for key in order:
        result[key] = unordered[key]
    return result
