import unittest

from util.cumulativelist import CumulativeList


class CumulativeListTestCase(unittest.TestCase):
    def test_append(self):
        l: CumulativeList[int] = CumulativeList(20)
        l.append(1)
        self.assertEqual(1, l[0])
        s = 1
        for i in range(1, 20):
            s += i
            l.append(i)
            self.assertEqual(s, l[i])
        for i in range(20):
            s += i
            l.append(i)
            self.assertEqual(s, l[i])

    def test_value(self):
        l: CumulativeList[int] = CumulativeList(20)
        l.append(1)
        self.assertEqual(1, l.value())
        for i in range(2, 21):
            l.append(1)
            self.assertEqual(i, l.value())
        for _ in range(100):
            l.append(1)
            self.assertEqual(20, l.value())


if __name__ == '__main__':
    unittest.main()
