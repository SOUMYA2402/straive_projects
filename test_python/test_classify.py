import pytest
from classify import classify


def test_even_numbers():
    assert classify(2) == "even"
    assert classify(10) == "even"
    assert classify(0) == "even"   # edge case


def test_divisible_by_three():
    assert classify(3) == "divisible by 3"
    assert classify(9) == "divisible by 3"


def test_other_numbers():
    assert classify(5) == "other"
    assert classify(7) == "other"


def test_priority_even_over_three():
    # 6 is divisible by 2 and 3, but should return "even" first
    assert classify(6) == "even"
