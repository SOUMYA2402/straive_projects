import pytest
from banking import Account, InsufficientBalanceError


# --------------------------
# 1. Fixture Setup
# --------------------------
@pytest.fixture
def accounts():
    acc1 = Account("Alice", 1000)
    acc2 = Account("Bob", 500)
    return acc1, acc2


# --------------------------
# 2. Deposit Tests
# --------------------------
def test_deposit_increases_balance(accounts):
    acc1, _ = accounts
    new_balance = acc1.deposit(200)
    assert new_balance == 1200
    assert acc1.balance == 1200


def test_deposit_invalid_amount(accounts):
    acc1, _ = accounts
    with pytest.raises(ValueError, match="Deposit must be positive"):
        acc1.deposit(0)

    with pytest.raises(ValueError, match="Deposit must be positive"):
        acc1.deposit(-50)


# --------------------------
# 3. Withdraw Tests
# --------------------------
def test_withdraw_decreases_balance(accounts):
    acc1, _ = accounts
    new_balance = acc1.withdraw(300)
    assert new_balance == 700
    assert acc1.balance == 700


def test_withdraw_insufficient_balance(accounts):
    acc1, _ = accounts
    with pytest.raises(InsufficientBalanceError, match="Not enough balance"):
        acc1.withdraw(2000)


# --------------------------
# 4. Transfer Tests
# --------------------------
def test_transfer_success(accounts):
    acc1, acc2 = accounts
    acc1.transfer(acc2, 400)
    assert acc1.balance == 600
    assert acc2.balance == 900


def test_transfer_insufficient_funds(accounts):
    acc1, acc2 = accounts
    with pytest.raises(InsufficientBalanceError, match="Not enough balance"):
        acc1.transfer(acc2, 2000)

    # balances remain unchanged
    assert acc1.balance == 1000
    assert acc2.balance == 500


# --------------------------
# 5. Parameterized Withdraw Test
# --------------------------
@pytest.mark.parametrize("amount", [100, 500, 1000])
def test_withdraw_various_amounts(accounts, amount):
    acc1, _ = accounts
    initial_balance = acc1.balance
    if amount <= initial_balance:
        acc1.withdraw(amount)
        assert acc1.balance == initial_balance - amount
    else:
        with pytest.raises(InsufficientBalanceError):
            acc1.withdraw(amount)


# --------------------------
# 6. Exception Message Validation
# --------------------------
def test_overdraft_exception_message(accounts):
    acc1, _ = accounts
    with pytest.raises(InsufficientBalanceError) as exc_info:
        acc1.withdraw(5000)
    assert str(exc_info.value) == "Not enough balance"


# --------------------------
# 7. Edge Case: Full Balance Transfer
# --------------------------
def test_full_balance_transfer(accounts):
    acc1, acc2 = accounts
    acc1.transfer(acc2, acc1.balance)
    assert acc1.balance == 0
    assert acc2.balance == 1500
