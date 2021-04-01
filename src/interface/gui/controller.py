import contextlib

# Suppress the pygame welcome message.
from simulator.statistics.vehicletype import VehicleType
from simulator.vehicle.emergency import EmergencyCar

with contextlib.redirect_stdout(None):
    import pygame

from interface.gui.colors import Colors, gradient, Color
from simulator.simulator import Simulator
from simulator.statistics.tracker import Tracker
from simulator.vehicle.autonomous import AutonomousCar
from simulator.vehicle.car import Car
from simulator.vehicle.obstacle import Obstacle
from simulator.vehicle.vehicle import Vehicle
from util.format import OptionalFormat

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

    def __init__(self, simulator: Simulator):
        self.simulator = simulator
        pygame.init()
        self.width = self.simulator.road.length * self.SIZE
        self.height = self.simulator.road.sublanesCount * self.SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('CAViar', 'CAViar')

    def run(self, speed: float = 100., refresh: int = 60, buffer: int = 1) -> None:
        # Initialize parameters.
        self.speed = speed
        self.passed = 0
        self.running = True
        self.clock = pygame.time.Clock()
        # Initialize statistics.
        with Tracker(simulator=self.simulator, buffer_size=buffer) as tracker:
            while self.running:
                self._updateEvents()
                if self._updateTime():
                    self.simulator.step()

                self.screen.fill(CL_ROAD)
                self._drawVehicles(self.passed / self.speed)
                self._drawStatistics(tracker)
                pygame.display.flip()
                pygame.display.update()
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
        x -= obstacle.length
        length = obstacle.length * self.SIZE
        width = obstacle.width * self.SIZE
        rect = (x * self.SIZE + 1, y * self.SIZE + 1, length - 2, width - 2)
        pygame.draw.rect(self.screen, CL_OBSTACLE, rect)

    def _drawVehicle(self, vehicle: Vehicle, factor: float) -> None:
        ax, ay = vehicle.last_position
        bx, by = vehicle.position
        x, y = ax + (bx - ax) * factor, ay + (by - ay) * factor
        x -= vehicle.length
        length = vehicle.length * self.SIZE
        width = vehicle.width * self.SIZE
        rect = (x * self.SIZE + 1, y * self.SIZE + 1, length - 2, width - 2)
        pygame.draw.rect(self.screen, self._getVehicleColor(vehicle), rect)

    def _getVehicleColor(self, vehicle: Vehicle) -> Color:
        limit = self.simulator.road.controller.getMaxSpeed(vehicle.position, width=vehicle.width)
        if isinstance(vehicle, AutonomousCar):
            start, end = Colors.PURPLE, Colors.BLUE
        elif isinstance(vehicle, EmergencyCar):
            start, end = Colors.WHITE, Colors.BLACK
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

    def _drawStatistics(self, tracker: Tracker) -> None:
        rect = (0, self.height, self.width, self.STATS_SIZE)
        pygame.draw.rect(self.screen, CL_BACKGROUND, rect)
        font = pygame.font.Font(pygame.font.get_default_font(), self.SIZE)
        statistics = {
            'steps': tracker.steps,
            'velocity': tracker.getAverageVelocity(VehicleType.ANY),
            'velocity_autonomous': tracker.getAverageVelocity(VehicleType.AUTONOMOUS),
            'velocity_conventional': tracker.getAverageVelocity(VehicleType.CONVENTIONAL),
        }
        text = font.render(
            'Steps={steps} | Velocity={velocity:.2f} | '
            'Conventional Velocity={velocity_conventional:.2f} | '
            'Autonomous Velocity={velocity_autonomous:.2f}'.format(
                **withOptionalFormat(statistics)), True, CL_TEXT)
        rect = text.get_rect()
        rect.center = (self.width // 2, self.height + self.STATS_SIZE // 2)
        self.screen.blit(text, rect)


def withOptionalFormat(statistics):
    return {k: OptionalFormat(v) for k, v in statistics.items()}
