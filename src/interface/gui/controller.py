import itertools
import typing

import pygame

from interface.gui.colors import Colors, gradient, Color
from simulator.simulator import Simulator
from simulator.statistics import Statistics
from simulator.vehicle.autonomous import AutonomousCar
from simulator.vehicle.car import Car
from simulator.vehicle.obstacle import Obstacle
from simulator.vehicle.vehicle import Vehicle

CL_OBSTACLE = Colors.DARK
CL_ROAD = Colors.LIGHT
CL_BACKGROUND = Colors.WHITE
CL_TEXT = Colors.BLACK


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
        for vehicle in itertools.chain(
                self.simulator.road.getAllVehicles(), self.simulator.road.removed):
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
        length = vehicle.length * self.SIZE
        rect = (x * self.SIZE + 1, y * self.SIZE + 1, length - 2, self.SIZE - 2)
        pygame.draw.rect(self.screen, self._getVehicleColor(vehicle), rect)

    def _getVehicleColor(self, vehicle: Vehicle) -> Color:
        limit = self.simulator.road.controller.getMaxSpeed(vehicle.position)
        if isinstance(vehicle, AutonomousCar):
            start, end = Colors.PURPLE, Colors.BLUE
        elif isinstance(vehicle, Car):
            start, end = Colors.RED, Colors.GREEN
        else:
            raise ValueError()
        color = gradient(start, end, .0 if limit == 0 else vehicle.velocity / limit)
        return color

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
            'Steps={steps} | Velocity={average_velocity:.2f} | '
            'Conventional Velocity={average_velocity_conventional:.2f} | '
            'Autonomous Velocity={average_velocity_autonomous:.2f}'.format(
                **withOptionalFormat(self.statistics)),
            True, CL_TEXT)
        rect = text.get_rect()
        rect.center = (self.width // 2, self.height + self.STATS_SIZE // 2)
        self.screen.blit(text, rect)


T = typing.TypeVar('T')


class OptionalFormat(typing.Generic[T]):  # The wrapper is not type-specific
    def __init__(self, value: typing.Optional[T]):
        self.value = value

    def __format__(self, *args, **kwargs) -> str:
        if self.value is None:
            return '~'
        else:
            return self.value.__format__(*args, **kwargs)


def withOptionalFormat(statistics: Statistics) -> Statistics:
    return {k: OptionalFormat(v) for k, v in statistics.items()}
