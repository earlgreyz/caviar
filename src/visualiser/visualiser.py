import pygame

from simulator.simulator import Simulator

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Visualiser:
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
            ax, ay = vehicle.last_position
            bx, by = vehicle.position
            x, y = ax + (bx - ax) * factor, ay + (by - ay) * factor
            rect = (x * self.SIZE, y * self.SIZE, self.SIZE, self.SIZE)
            pygame.draw.rect(self.screen, BLACK, rect)

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
        self.screen.fill(WHITE)
        self.drawVehicles(passed / speed)
        pygame.display.flip()
        pygame.display.update()
