import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):

    def setUp(self):
        """Create a Calculator instance for each test."""
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(4, 2.5), 10.0)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)

    def test_divide_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(1, 0)

    def test_power(self):
        self.assertEqual(self.calc.power(2, 3), 8)

    def test_sqrt(self):
        self.assertEqual(self.calc.sqrt(9), 3)

    def test_sqrt_negative(self):
        with self.assertRaises(ValueError):
            self.calc.sqrt(-4)

    def test_percent(self):
        self.assertEqual(self.calc.percent(200, 10), 20)


if __name__ == '__main__':
    unittest.main()
