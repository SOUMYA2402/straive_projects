import pytest
from chain_transaction import Account, InsufficientBalanceError

@pytest.fixture
def accounts():
    acc1 = Account("Alice", 1000)
    acc2 = Account("Bob", 500)
    return acc1, acc2

def test_chained_transactions(accounts):
    acc1, acc2 = accounts


    total_credits = 0
    total_debits = 0


    acc1.deposit(2000)
    total_credits += 2000


    acc1.withdraw(500)
    total_debits += 500


    acc1.transfer(acc2, 1000)
    total_debits += 1000


    assert acc1.balance == 1500
    assert acc2.balance == 1500


    assert total_credits == 2000
    assert total_debits == 1500
