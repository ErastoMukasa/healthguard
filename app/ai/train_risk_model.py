# app/ai/train_risk_model.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib
import os

# Example simulated data (replace with real patient data if available)
def generate_sample_data():
    import numpy as np
    np.random.seed(42)
    data = {
        "temperature": np.random.normal(37, 1, 500),
        "heart_rate": np.random.normal(75, 10, 500),
        "oxygen_level": np.random.normal(97, 2, 500),
        "glucose_level": np.random.normal(100, 15, 500),
        "blood_pressure": np.random.normal(120, 15, 500),
        "risk": np.random.randint(0, 2, 500)  # 0: low risk, 1: high risk
    }
    return pd.DataFrame(data)

# Step 1: Load your data (here simulated)
df = generate_sample_data()

# Step 2: Preprocessing
X = df[["temperature", "heart_rate", "oxygen_level", "glucose_level", "blood_pressure"]]
y = df["risk"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 4: Train Logistic Regression
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 5: Evaluate
y_pred = model.predict(X_test)
print("Model Evaluation:\n", classification_report(y_test, y_pred))

# Step 6: Save model and scaler
model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.joblib')
joblib.dump(model, model_path)
joblib.dump(scaler, scaler_path)
print(f"Model saved to {model_path}")
