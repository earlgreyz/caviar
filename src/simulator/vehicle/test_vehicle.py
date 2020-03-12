import unittest

from simulator.vehicle.vehicle import Vehicle


class TestVehicle(unittest.TestCase):
    def test_init(self):
        # Default velocity.
        vehicle = Vehicle(position=(42, 2))
        self.assertEqual(vehicle.velocity, 0, 'velocity not initialized')
        x, lane = vehicle.position
        self.assertEqual(x, 42, 'position x differs')
        self.assertEqual(lane, 2, 'position lane differs')
        x, lane = vehicle.last_position
        self.assertEqual(x, 42, 'last position x differs')
        self.assertEqual(lane, 2, 'last position lane differs')
        # Non default velocity.
        vehicle = Vehicle(position=(42, 2), velocity=10)
        self.assertEqual(vehicle.velocity, 10, 'velocity differs')
        x, lane = vehicle.position
        self.assertEqual(x, 42, 'position x differs')
        self.assertEqual(lane, 2, 'position lane differs')
        x, lane = vehicle.last_position
        self.assertEqual(x, 42, 'last position x differs')
        self.assertEqual(lane, 2, 'last position lane differs')

    def test_interface(self):
        vehicle = Vehicle(position=(0, 0))
        with self.assertRaises(NotImplementedError, msg='expected beforeMove to be virtual'):
            vehicle.beforeMove()
        with self.assertRaises(NotImplementedError, msg='expected move to be virtual'):
            vehicle.move()


def testImplementsVehicle(self: unittest.TestCase, vehicle: Vehicle):
    position = vehicle.position
    try:
        vehicle.beforeMove()
        vehicle.move()
    except NotImplementedError:
        self.fail('Vehicle interface not implemented')
    self.assertEqual(vehicle.last_position, position, 'Last position differs')


if __name__ == '__main__':
    unittest.main()
