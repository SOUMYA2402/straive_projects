import pandas as pd

data = {
    "account_number": [1001, 1002, 1003],
    "customer_name": ["Anita Sharma", "Ravi Kumar", "Meena Joshi"],
    "account_type": ["Savings", "Checking", "Savings"],
    "balance": [15000.50, 8200.00, None],
    "last_transaction": ["2025-09-15", "2025-10-01", "2025-08-20"],
    "branch_code": ["S001", "S002", "S003"],
    "phone_number": ["9876543210", "9876543211", "9876543212"]
}

df = pd.DataFrame(data)
df.to_csv("bank_data.csv", index=False)
