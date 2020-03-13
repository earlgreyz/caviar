import unittest

from simulator.vehicle.vehicle import Vehicle


def implementsVehicle(cls):
    assert hasattr(cls, 'getVehicle') and callable(getattr(cls, 'getVehicle'))

    def test(self: cls):
        vehicle: Vehicle = self.getVehicle()
        position = vehicle.position
        try:
            vehicle.beforeMove()
            vehicle.move()
        except NotImplementedError:
            self.fail('Vehicle interface not implemented')
        self.assertEqual(vehicle.last_position, position, 'Last position differs')

    cls.test_implementsVehicle = test
    return cls


class VehicleTestCase(unittest.TestCase):
    def test_init(self):
        position = (42, 2)
        # Default velocity.
        vehicle = Vehicle(position=position)
        self.assertEqual(vehicle.velocity, 0, 'velocity not initialized')
        self.assertEqual(vehicle.position, position, 'positions differs')
        self.assertEqual(vehicle.last_position, position, 'last position not initialized')
        # Non default velocity.
        velocity = 10
        vehicle = Vehicle(position=position, velocity=velocity)
        self.assertEqual(vehicle.velocity, velocity, 'velocity differs')
        self.assertEqual(vehicle.position, position, 'positions differs')
        self.assertEqual(vehicle.last_position, position, 'last position not initialized')

    def test_interface(self):
        vehicle = Vehicle(position=(0, 0))
        with self.assertRaises(NotImplementedError, msg='expected beforeMove to be virtual'):
            vehicle.beforeMove()
        with self.assertRaises(NotImplementedError, msg='expected move to be virtual'):
            vehicle.move()


if __name__ == '__main__':
    unittest.main()
