import unittest

from util.sizedlist import SizedList


class SizedListTestCase(unittest.TestCase):
    def test_insert(self):
        l: SizedList[int] = SizedList(20)
        for i in range(100):
            l.insert(i)
            self.assertIn(i, l.items)

    def test_len(self):
        l: SizedList[int] = SizedList(20)
        # Check length grows up to the specified size.
        for i in range(20):
            l.insert(i)
            self.assertEqual(i + 1, len(l))
        # Check the list remains the specified size.
        for i in range(20):
            l.insert(20 + i)
            self.assertEqual(20, len(l))

    def test_iter(self):
        l: SizedList[int] = SizedList(20)
        for i in range(20):
            l.insert(i)
        # Check initial list.
        self.assertListEqual(list(range(20)), list((i for i in l)))
        # Check first item gets replaced.
        for i in range(20):
            l.insert(20 + i)
            self.assertListEqual(list(range(i + 1, 20 + i + 1)), list((i for i in l)))

    def test_getitem(self):
        l: SizedList[int] = SizedList(20)
        for i in range(20):
            l.insert(i)
        # Check initial getitem.
        for i in range(20):
            self.assertEqual(i, l[i])
        # Check first item gets replaced and start is moved.
        for i in range(20):
            l.insert(20 + i)
            self.assertListEqual(list(range(i + 1, 20 + i + 1)), list((l[i] for i in range(20))))


if __name__ == '__main__':
    unittest.main()
