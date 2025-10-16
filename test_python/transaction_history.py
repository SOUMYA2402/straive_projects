
class InsufficientBalanceError(Exception):
    pass



class InsufficientBalanceError(Exception):
    pass


class Account:
    def __init__(self, owner, balance=0, annual_rate=0.05):
        self.owner = owner
        self.balance = balance
        self.annual_rate = annual_rate
        self.history = []
        if balance > 0:
            self.history.append(('Initial', balance))

    def deposit(self, amount, log_history=True):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount
        if log_history:
            self.history.append(('Deposit', amount, self.balance))
        return self.balance

    def withdraw(self, amount, log_history=True):
        if amount > self.balance:
            raise InsufficientBalanceError("Not enough balance")
        self.balance -= amount
        if log_history:
            self.history.append(('Withdraw', amount, self.balance))
        return self.balance

    def transfer(self, target_account, amount):
        # Withdraw and deposit without logging individual entries
        self.withdraw(amount, log_history=False)
        target_account.deposit(amount, log_history=False)

        # Only log the transfer entries
        self.history.append(('Transfer Out', amount, self.balance))
        target_account.history.append(('Transfer In', amount, target_account.balance))

        return (self.balance, target_account.balance)

    def apply_annual_interest(self):
        interest = self.balance * self.annual_rate
        self.balance += interest
        self.history.append(('Interest', interest, self.balance))
        return interest


def calculate_emi(principal, annual_rate, years):
    r = annual_rate / 12
    n = years * 12
    emi = (principal * r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return round(emi, 2)


