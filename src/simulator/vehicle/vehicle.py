import enum

from simulator.position import Position


class VehicleFlags(enum.Flag):
    NONE = 0
    MOVED = enum.auto()


class Vehicle:
    # Vehicle properties.
    position: Position
    velocity: int
    length: int
    width: int

    # Runtime properties.
    last_position: Position
    flags: VehicleFlags

    def __init__(self, position: Position, velocity: int = 0, length: int = 1, width: int = 1):
        self.position = position
        self.velocity = velocity
        self.length = length
        self.width = width
        self.last_position = position
        self.flags = VehicleFlags.NONE

    def beforeMove(self) -> Position:
        '''
        Called for all vehicles on the road before performing the actual action.
        :return: new position.
        '''
        raise NotImplementedError

    def move(self) -> Position:
        '''
        Called for all vehicles on the road in every step of the simulation.
        :return: new position.
        '''
        raise NotImplementedError
