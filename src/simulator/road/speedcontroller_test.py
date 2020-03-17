import unittest

from simulator.road.speedcontroller import SpeedController


class SpeedControllerTestCase(unittest.TestCase):
    def test_getMaxSpeed(self):
        # Default max speed.
        controller = SpeedController()
        speed = controller.getMaxSpeed(position=(10, 0))
        self.assertEqual(speed, 5, 'invalid default max speed')
        speed = controller.getMaxSpeed(position=(42, 1))
        self.assertEqual(speed, 5, 'invalid default max speed')
        # Custom max speed.
        controller = SpeedController(max_speed=10)
        speed = controller.getMaxSpeed(position=(10, 0))
        self.assertEqual(speed, 10, 'invalid max speed')
        speed = controller.getMaxSpeed(position=(42, 1))
        self.assertEqual(speed, 10, 'invalid max speed')
        # Partial limits.
        controller = SpeedController(max_speed=10)
        controller.addLimit(0, 10, 20, 5)
        speed = controller.getMaxSpeed(position=(9, 0))
        self.assertEqual(speed, 10, 'invalid limit')
        speed = controller.getMaxSpeed(position=(21, 0))
        self.assertEqual(speed, 10, 'invalid limit')
        speed = controller.getMaxSpeed(position=(10, 0))
        self.assertEqual(speed, 5, 'invalid limit')
        speed = controller.getMaxSpeed(position=(15, 0))
        self.assertEqual(speed, 5, 'invalid limit')
        speed = controller.getMaxSpeed(position=(20, 0))
        self.assertEqual(speed, 5, 'invalid limit')
        # Multiple limits should return the lowers.
        controller = SpeedController(max_speed=10)
        controller.addLimit(0, 10, 20, 5)
        controller.addLimit(0, 15, 25, 3)
        speed = controller.getMaxSpeed(position=(9, 0))
        self.assertEqual(speed, 10, 'invalid limit')
        speed = controller.getMaxSpeed(position=(26, 0))
        self.assertEqual(speed, 10, 'invalid limit')
        speed = controller.getMaxSpeed(position=(10, 0))
        self.assertEqual(speed, 5, 'invalid limit')
        speed = controller.getMaxSpeed(position=(14, 0))
        self.assertEqual(speed, 5, 'invalid limit')
        speed = controller.getMaxSpeed(position=(15, 0))
        self.assertEqual(speed, 3, 'invalid limit')
        speed = controller.getMaxSpeed(position=(25, 0))
        self.assertEqual(speed, 3, 'invalid limit')


if __name__ == '__main__':
    unittest.main()
