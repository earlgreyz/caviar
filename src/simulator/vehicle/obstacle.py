from simulator.position import Position
from simulator.vehicle.vehicle import Vehicle


class Obstacle(Vehicle):
    def __init__(self, position: Position):
        super().__init__(position=position, velocity=0)

    def beforeMove(self) -> Position:
        return self.position

    def move(self) -> Position:
        return self.position
