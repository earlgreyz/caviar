import enum

from simulator.position import Position


class VehicleFlags(enum.Flag):
    NONE = 0
    MOVED = enum.auto()
    CHANGED = enum.auto()
    NICE = enum.auto()


class Vehicle:
    position: Position
    last_position: Position
    velocity: int
    length: int

    flags: VehicleFlags

    def __init__(self, position: Position, velocity: int = 0, length: int = 1):
        self.position = position
        self.last_position = position
        self.velocity = velocity
        self.length = length
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

    def isEmergencyVehicle(self) -> bool:
        '''
        Returns whether a vehicle is an emergency vehicle.
        :return: if a vehicle is an emergency vehicle.
        '''
        return False
