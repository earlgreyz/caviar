from simulator.position import Position


class Vehicle:
    position: Position
    last_position: Position
    velocity: int
    length: int
    moved: bool

    def __init__(self, position: Position, velocity: int = 0, length: int = 1):
        self.position = position
        self.last_position = position
        self.velocity = velocity
        self.length = length

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
