import enum
import unittest

from util.enum import withLimits


class EnumTestCase(unittest.TestCase):
    def test_withLimits(self):
        # Check ALL is not added to empty enum.
        @withLimits
        class TestEnum(enum.Flag):
            pass

        with self.assertRaises(AttributeError):
            _ = TestEnum.ALL

        # Check NONE is a neutral flag.
        @withLimits
        class TestEnum(enum.Flag):
            FIRST = enum.auto()
            SECOND = enum.auto()

        self.assertFalse(TestEnum.NONE)
        self.assertEqual(TestEnum.NONE | TestEnum.FIRST, TestEnum.FIRST)
        self.assertEqual(TestEnum.NONE | TestEnum.SECOND, TestEnum.SECOND)
        self.assertNotEqual(TestEnum.FIRST | TestEnum.SECOND, TestEnum.FIRST)
        self.assertNotEqual(TestEnum.FIRST | TestEnum.SECOND, TestEnum.SECOND)

        # Check ALL has all the flags.
        self.assertTrue(TestEnum.ALL & TestEnum.FIRST)
        self.assertTrue(TestEnum.ALL & TestEnum.SECOND)


if __name__ == '__main__':
    unittest.main()
