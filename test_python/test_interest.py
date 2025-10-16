import pytest
from interest import Account


@pytest.fixture
def accounts():
    acc1 = Account("Alice", 1000, annual_rate=0.05)
    acc2 = Account("Bob", 2000, annual_rate=0.03)
    return acc1, acc2



def test_annual_interest(accounts):
    acc1, acc2 = accounts
    assert acc1.calculate_annual_interest() == 50.0
    assert acc2.calculate_annual_interest() == 60.0


def test_annual_interest_zero_balance():
    acc = Account("Charlie", 0, annual_rate=0.1)
    assert acc.calculate_annual_interest() == 0.0


def test_compound_interest_yearly(accounts):
    acc1, _ = accounts

    assert acc1.calculate_compound_interest(years=2, compounding_frequency=1) == 1102.5
    assert acc1.calculate_compound_interest(years=0, compounding_frequency=1) == 1000.0


def test_compound_interest_quarterly(accounts):
    acc1, _ = accounts

    assert acc1.calculate_compound_interest(years=1, compounding_frequency=4) == 1050.95
    assert acc1.calculate_compound_interest(years=2, compounding_frequency=4) == 1104.67


def test_compound_interest_zero_balance():
    acc = Account("Charlie", 0, annual_rate=0.1)
    assert acc.calculate_compound_interest(years=5, compounding_frequency=4) == 0.0



@pytest.mark.parametrize("years,expected", [
    (0, 1000.0),
    (1, 1050.0),
    (2, 1102.5),
    (5, 1276.28),
])
def test_parameterized_compound_interest(years, expected):
    acc = Account("Alice", 1000, annual_rate=0.05)
    assert acc.calculate_compound_interest(years=years) == expected
