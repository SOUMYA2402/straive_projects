import pytest
from transaction_history import Account, calculate_emi, InsufficientBalanceError

@pytest.mark.parametrize("principal,rate,years,expected_emi", [
    (100000, 0.06, 1, 8606.64),
    (100000, 0.06, 5, 1933.28),
    (100000, 0.06, 30, 599.55),
])
def test_emi_calculation(principal, rate, years, expected_emi):
    assert calculate_emi(principal, rate, years) == expected_emi
    total_paid = expected_emi*12*years
    assert total_paid > principal




def test_transaction_history():
    acc = Account("Alice", 1000)
    acc.deposit(500)
    acc.withdraw(300)

    assert len(acc.history) == 3
    assert acc.history[-1][0] == 'Withdraw'
    assert acc.history[-1][2] == acc.balance  # last entry reflects final balance


def test_full_year_simulation():
    acc = Account("Alice", 20000, annual_rate=0.06)


    for _ in range(12):
        acc.deposit(500)


    acc.apply_annual_interest()


    acc.withdraw(3000)


    initial = 20000
    monthly_deposit = 500
    balance_before_interest = initial + monthly_deposit*12
    interest = balance_before_interest * 0.06
    final_balance = balance_before_interest + interest - 3000

    assert acc.balance == round(final_balance, 2)


def test_zero_interest():
    acc = Account("Bob", 10000, annual_rate=0.0)
    acc.apply_annual_interest()
    assert acc.balance == 10000

def test_negative_interest():
    acc = Account("Charlie", 10000, annual_rate=-0.05)
    acc.apply_annual_interest()
    expected_balance = 10000 * (1 - 0.05)
    assert acc.balance == round(expected_balance, 2)
