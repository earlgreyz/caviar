import pygame

from simulator.simulator import Simulator
from simulator.vehicle.obstacle import Obstacle
from simulator.vehicle.vehicle import Vehicle

CL_OBSTACLE = (67, 67, 78)
CL_ROAD = (212, 212, 212)
CL_VEHICLE = (27, 176, 66)


class Controller:
    SIZE = 10
    simulator: Simulator

    def __init__(self, simulator: Simulator):
        self.simulator = simulator
        pygame.init()
        width = self.simulator.road.length * self.SIZE
        height = self.simulator.road.lanes_count * self.SIZE
        self.screen = pygame.display.set_mode((width, height))

    def drawVehicles(self, factor: float):
        for vehicle in self.simulator.road.getAllVehicles():
            if isinstance(vehicle, Obstacle):
                self.drawObstacle(vehicle)
            else:
                self.drawVehicle(vehicle, factor)

    def drawObstacle(self, obstacle: Obstacle):
        x, y = obstacle.position
        rect = (x * self.SIZE, y * self.SIZE, self.SIZE, self.SIZE)
        pygame.draw.rect(self.screen, CL_OBSTACLE, rect)

    def drawVehicle(self, vehicle: Vehicle, factor: float):
        ax, ay = vehicle.last_position
        bx, by = vehicle.position
        x, y = ax + (bx - ax) * factor, ay + (by - ay) * factor
        rect = (x * self.SIZE, y * self.SIZE, self.SIZE, self.SIZE)
        pygame.draw.ellipse(self.screen, CL_VEHICLE, rect)

    def run(self, speed: float = 100., refresh: int = 60):
        clock = pygame.time.Clock()

        running = True
        passed = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            dt = clock.get_time()
            passed += dt
            if passed > speed:
                passed = passed % speed
                self.simulator.step()

            self.draw(passed, speed)
            clock.tick(refresh)
        pygame.quit()

    def draw(self, passed: float, speed: float):
        self.screen.fill(CL_ROAD)
        self.drawVehicles(passed / speed)
        pygame.display.flip()
        pygame.display.update()
