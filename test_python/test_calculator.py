
import pytest
from calculator import Calculator


@pytest.fixture
def calc():
    """Fixture to provide a Calculator instance for all tests."""
    return Calculator()


class TestCalculator:

    def test_add(self, calc):
        assert calc.add(2, 3) == 5
        assert calc.add(-1, 1) == 0

    def test_subtract(self, calc):
        assert calc.subtract(5, 3) == 2

    def test_multiply(self, calc):
        assert calc.multiply(4, 2.5) == 10.0

    def test_divide(self, calc):
        assert calc.divide(10, 2) == 5

    def test_divide_zero(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(1, 0)

    def test_power(self, calc):
        assert calc.power(2, 3) == 8

    def test_sqrt(self, calc):
        assert calc.sqrt(9) == 3

    def test_sqrt_negative(self, calc):
        with pytest.raises(ValueError):
            calc.sqrt(-4)

    def test_percent(self, calc):
        assert calc.percent(200, 10) == 20
