# Import libraries
import pandas as pd
# import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
awr6efq6# from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Load dataset
df = pd.read_csv('netflix_titles.csv')

# Drop rows with missing title or type
df.dropna(subset=['title', 'type'], inplace=True)

# Fill missing values
df['director'].fillna('Unknown', inplace=True)
df['cast'].fillna('Unknown', inplace=True)
df['country'].fillna('Unknown', inplace=True)
df['rating'].fillna('NR', inplace=True)
df['duration'].fillna('0 min', inplace=True)

# Extract duration in minutes
df['duration_min'] = df['duration'].str.extract('(\d+)').astype(float)
df['duration_min'].fillna(df['duration_min'].median(), inplace=True)

# Feature engineering
df['num_cast'] = df['cast'].apply(lambda x: len(x.split(',')) if x != 'Unknown' else 0)
df['num_genres'] = df['listed_in'].apply(lambda x: len(x.split(',')) if pd.notnull(x) else 0)
df['is_recent'] = (df['release_year'] >= 2015).astype(int)
df['is_movie'] = (df['type'] == 'Movie').astype(int)

# Simulate target: popular if duration > 90 or rating is TV-MA/TV-14
df['popular'] = ((df['duration_min'] > 90) | (df['rating'].isin(['TV-MA', 'TV-14']))).astype(int)

# Select features
features = ['country', 'rating', 'release_year', 'duration_min', 'num_cast', 'num_genres', 'is_recent', 'is_movie']
X = df[features]
y = df['popular']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# Preprocessing
categorical = ['country', 'rating']
numerical = ['release_year', 'duration_min', 'num_cast', 'num_genres', 'is_recent', 'is_movie']

preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), numerical),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical)
])

# Models
models = {
    'LogisticRegression': LogisticRegression(max_iter=1000),
    'RandomForest': RandomForestClassifier(n_estimators=100),
    'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='logloss')
}

# Train and evaluate
for name, model in models.items():
    pipe = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]
    print(f"\nModel: {name}")
    print(classification_report(y_test, y_pred))
    print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")

# Example prediction
example = pd.DataFrame([{
    'country': 'United States',
    'rating': 'PG-13',
    'release_year': 2010,
    'duration_min': 148,
    'num_cast': 5,
    'num_genres': 2,
    'is_recent': 0,
    'is_movie': 1
}])

# Use XGBoost pipeline for prediction
xgb_pipe = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', models['XGBoost'])])
xgb_pipe.fit(X_train, y_train)
pred = xgb_pipe.predict(example)
proba = xgb_pipe.predict_proba(example)[0][1]

print("\n🔍 Example Prediction:")
print(f"Predicted Popularity: {'Popular' if pred[0] == 1 else 'Not Popular'}")
print(f"Confidence Score: {proba:.2f}")
