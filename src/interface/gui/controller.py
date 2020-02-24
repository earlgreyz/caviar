import pygame

from simulator.simulator import Simulator
from simulator.statistics import Statistics
from simulator.vehicle.obstacle import Obstacle
from simulator.vehicle.vehicle import Vehicle

CL_OBSTACLE = (67, 67, 78)
CL_ROAD = (212, 212, 212)
CL_VEHICLE = (27, 176, 66)
CL_BACKGROUND = (255, 255, 255)
CL_TEXT = (0, 0, 0)


class Controller:
    simulator: Simulator
    # GUI constants.
    SIZE = 10
    STATS_SIZE = 30
    # GUI parameters.
    width: int
    height: int
    # Animation parameters.
    running: bool
    passed: float
    speed: float
    clock: pygame.time.Clock
    statistics: Statistics

    def __init__(self, simulator: Simulator):
        self.simulator = simulator
        pygame.init()
        self.width = self.simulator.road.length * self.SIZE
        self.height = self.simulator.road.lanes_count * self.SIZE
        self.screen = pygame.display.set_mode((self.width, self.height + self.STATS_SIZE))

    def run(self, speed: float = 100., refresh: int = 60) -> None:
        # Initialize parameters.
        self.speed = speed
        self.passed = 0
        self.running = True
        self.clock = pygame.time.Clock()
        # Initialize statistics.
        self.statistics: Statistics = self.simulator.step()
        while self.running:
            self._updateEvents()
            if self._updateTime():
                self.statistics = self.simulator.step()
            self._draw()
            self.clock.tick(refresh)
        pygame.quit()

    def _drawVehicles(self, factor: float) -> None:
        for vehicle in self.simulator.road.getAllVehicles():
            if isinstance(vehicle, Obstacle):
                self._drawObstacle(vehicle)
            else:
                self._drawVehicle(vehicle, factor)

    def _drawObstacle(self, obstacle: Obstacle) -> None:
        x, y = obstacle.position
        rect = (x * self.SIZE, y * self.SIZE, self.SIZE, self.SIZE)
        pygame.draw.rect(self.screen, CL_OBSTACLE, rect)

    def _drawVehicle(self, vehicle: Vehicle, factor: float) -> None:
        ax, ay = vehicle.last_position
        bx, by = vehicle.position
        x, y = ax + (bx - ax) * factor, ay + (by - ay) * factor
        rect = (x * self.SIZE, y * self.SIZE, self.SIZE, self.SIZE)
        pygame.draw.ellipse(self.screen, CL_VEHICLE, rect)

    def _updateEvents(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _updateTime(self) -> bool:
        dt = self.clock.get_time()
        self.passed += dt
        if self.passed > self.speed:
            self.passed = self.passed % self.speed
            return True
        return False

    def _draw(self) -> None:
        self.screen.fill(CL_ROAD)
        self._drawVehicles(self.passed / self.speed)
        self._drawStatistics()
        pygame.display.flip()
        pygame.display.update()

    def _drawStatistics(self) -> None:
        rect = (0, self.height, self.width, self.STATS_SIZE)
        pygame.draw.rect(self.screen, CL_BACKGROUND, rect)
        font = pygame.font.Font(pygame.font.get_default_font(), self.SIZE)
        text = font.render(
            'Steps={steps}, Velocity={average_velocity:.2f}'.format(**self.statistics),
            True, CL_TEXT)
        rect = text.get_rect()
        rect.center = (self.width // 2, self.height + self.STATS_SIZE // 2)
        self.screen.blit(text, rect)
