"""Simple calculator module with OOP design."""
import math
from typing import Union

Number = Union[int, float]


class Calculator:
    """A simple calculator exposing common operations."""

    def add(self, a: Number, b: Number) -> Number:
        return a + b

    def subtract(self, a: Number, b: Number) -> Number:
        return a - b

    def multiply(self, a: Number, b: Number) -> Number:
        return a * b

    def divide(self, a: Number, b: Number) -> Number:
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b

    def power(self, a: Number, b: Number) -> Number:
        return a ** b

    def sqrt(self, a: Number) -> Number:
        if a < 0:
            raise ValueError("sqrt of negative number")
        return math.sqrt(a)

    def percent(self, value: Number, pct: Number) -> Number:
        """Return `pct` percent of `value`. Example: percent(200, 10) -> 20"""
        return (value * pct) / 100


if __name__ == '__main__':
    calc = Calculator()
    print('2 + 3 =', calc.add(2, 3))
    print('sqrt(16) =', calc.sqrt(16))
