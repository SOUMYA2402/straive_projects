
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import  LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix, classification_report

df = pd.read_csv("diabetes.csv")
print("Dataset shape:", df.shape)
print(df.head())


X = df.drop("Outcome", axis=1)   # these are the Features
y = df["Outcome"]                # we need to predict this (we treat it as regression)

# Step 3: Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 4: Train Linear Logistic model
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 5: Make predictions
y_pred = model.predict(X_test)

#Making Confusion Matrix
print("Accuracy:", accuracy_score(y_test,y_pred))
print("\n Confusion Matrix: \n",confusion_matrix(y_test,y_pred))
print("\n Classification Report: \n",classification_report(y_test,y_pred))

# # Step 6: Evaluate model
# print("Intercept:", model.intercept_)
# print("Coefficients:", model.coef_)
# print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
# print("R² Score:", r2_score(y_test, y_pred))
