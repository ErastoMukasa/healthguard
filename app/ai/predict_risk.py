# app/ai/predict_risk.py

import joblib
import os
import numpy as np

# Load model and scaler once when module is imported
model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.joblib')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

def predict_risk(temperature, heart_rate, oxygen_level, glucose_level, blood_pressure):
    """
    Input features:
      - temperature: float (°C)
      - heart_rate: float (bpm)
      - oxygen_level: float (%)
      - glucose_level: float (mg/dL)
      - blood_pressure: float (systolic mmHg)

    Returns:
      - risk_class: int (0 = low risk, 1 = high risk)
      - risk_prob: float (probability of high risk, between 0 and 1)
    """

    # Prepare input array for scaler and model
    input_data = np.array([[temperature, heart_rate, oxygen_level, glucose_level, blood_pressure]])

    # Scale inputs
    input_scaled = scaler.transform(input_data)

    # Predict class and probability
    risk_class = model.predict(input_scaled)[0]
    risk_prob = model.predict_proba(input_scaled)[0][1]  # Probability for class 1 (high risk)

    return risk_class, risk_prob
