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
        raise NotImplementedError

    def move(self) -> Position:
        raise NotImplementedError
