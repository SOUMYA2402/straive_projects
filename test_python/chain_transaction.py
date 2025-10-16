

class InsufficientBalanceError(Exception):
    """Custom exception for insufficient account balance."""
    pass


class Account:
    def __init__(self, owner, balance=0, annual_rate=0.05):

        self.owner = owner
        self.balance = balance
        self.annual_rate = annual_rate


    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount
        return self.balance


    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientBalanceError("Not enough balance")
        self.balance -= amount
        return self.balance


    def transfer(self, target_account, amount):
        """
        Transfer money from this account to target_account.
        Raises InsufficientBalanceError if balance insufficient.
        Returns tuple (self.balance, target_account.balance)
        """
        self.withdraw(amount)
        target_account.deposit(amount)
        return (self.balance, target_account.balance)

    # ------------------- Simple Interest -------------------
    def calculate_annual_interest(self):
        """Simple interest: Balance * Rate"""
        return round(self.balance * self.annual_rate, 2)

    # ------------------- Compound Interest -------------------
    def calculate_compound_interest(self, years, compounding_frequency=1):
        """
        Compound Interest Formula:
        A = P * (1 + r/n)^(n*t)
        Returns final amount after compounding, rounded to 2 decimals.
        :param years: number of years
        :param compounding_frequency: times interest is compounded per year
        """
        P = self.balance
        r = self.annual_rate
        n = compounding_frequency
        t = years
        A = P * ((1 + r / n) ** (n * t))
        return round(A, 2)
