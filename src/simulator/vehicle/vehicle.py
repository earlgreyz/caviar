from simulator.position import Position


class Vehicle:
    position: Position
    last_position: Position
    velocity: int

    def __init__(self, position: Position, velocity: int = 0):
        self.position = position
        self.last_position = position
        self.velocity = velocity

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
