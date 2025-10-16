import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Sample dataset (Age, Salary, HighIncome?)
data = {
    "Age": [22, 25, 47, 52, 46, 56, 55, 60, 18, 35],
    "Salary": [20000, 25000, 50000, 60000, 80000, 85000, 90000, 95000, 15000, 40000],
    "HighIncome": [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]  # 0 = Low, 1 = High
}

df = pd.DataFrame(data)

# Features and labels
X = df[["Age", "Salary"]]
y = df["HighIncome"]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
print("✅ Model trained and saved as model.pkl")
