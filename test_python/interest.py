class InsufficientBalanceError(Exception):
    pass


class Account:
    def __init__(self, owner, balance=0, annual_rate=0.05):
        """
        :param owner: Account holder name
        :param balance: Initial balance
        :param annual_rate: Annual interest rate (default 5%)
        """
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

    def calculate_annual_interest(self):
        """
        Formula: Interest = Balance * Rate
        """
        return round(self.balance * self.annual_rate, 2)

    def calculate_compound_interest(self, years, compounding_frequency=1):
        """
        Formula: A = P * (1 + r/n)^(n*t)
        Returns final amount after compounding.
        """
        P = self.balance
        r = self.annual_rate
        n = compounding_frequency
        t = years
        A = P * ((1 + r / n) ** (n * t))
        return round(A, 2)