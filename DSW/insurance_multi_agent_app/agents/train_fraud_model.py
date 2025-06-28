import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Create "agents" folder if not exists
os.makedirs("agents", exist_ok=True)

# Generate synthetic dataset
np.random.seed(42)
n_samples = 1000

data = pd.DataFrame({
    'customer_age': np.random.randint(18, 80, n_samples),
    'claim_amount': np.random.randint(1000, 100000, n_samples),
    'policy_coverage': np.random.randint(20000, 200000, n_samples),
    'monthly_income': np.random.randint(10000, 100000, n_samples),
    'incident_type': np.random.choice(['Theft', 'Accident', 'Fire'], n_samples),
    'report_delay_days': np.random.randint(0, 60, n_samples),
    'doctor_certificate': np.random.choice(['Yes', 'No'], n_samples),
    'police_report': np.random.choice(['Yes', 'No'], n_samples),
    'months_after_policy': np.random.randint(1, 60, n_samples)
})

def label_fraud(row):
    if (
        row['report_delay_days'] > 30 or
        (row['doctor_certificate'] == 'No' and row['incident_type'] == 'Accident') or
        (row['police_report'] == 'No' and row['incident_type'] == 'Theft') or
        row['claim_amount'] > row['policy_coverage'] * 0.9
    ):
        return 'Yes'
    else:
        return 'No'

data['fraud_reported'] = data.apply(label_fraud, axis=1)

# Preprocess
X = data.drop('fraud_reported', axis=1)
y = data['fraud_reported']
X = pd.get_dummies(X, columns=['incident_type', 'doctor_certificate', 'police_report'], drop_first=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and feature list
joblib.dump(model, "insurance_multi_agent_app/fraud_model.pkl")
joblib.dump(X.columns, "insurance_multi_agent_app/feature_order.pkl")

print("✅ Model and features saved in /agents/")
