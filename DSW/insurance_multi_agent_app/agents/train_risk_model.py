import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Ensure the 'agents' directory exists
os.makedirs("agents", exist_ok=True)

# Generate synthetic underwriting risk data
np.random.seed(42)
n = 1000

data = pd.DataFrame({
    "age": np.random.randint(18, 80, size=n),
    "income": np.random.randint(10000, 200000, size=n),
    "health": np.random.choice(["Healthy", "Diabetic", "Hypertension", "Both"], size=n),
    "smoker": np.random.choice(["Smoker", "Non-Smoker"], size=n),
    "claim_history": np.random.choice(["Yes", "No"], size=n)
})

# Risk scoring logic
def assign_risk(row):
    score = 0
    if row["age"] > 60: score += 2
    if row["income"] < 30000: score += 1
    if row["health"] in ["Diabetic", "Hypertension"]: score += 1
    if row["health"] == "Both": score += 2
    if row["smoker"] == "Smoker": score += 2
    if row["claim_history"] == "Yes": score += 1
    if score <= 2:
        return "Low"
    elif score <= 4:
        return "Moderate"
    else:
        return "High"

# Apply label
data["risk"] = data.apply(assign_risk, axis=1)

# One-hot encode inputs
X = pd.get_dummies(data.drop("risk", axis=1), drop_first=True)
y = data["risk"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ✅ Save model
joblib.dump(model, "risk_model.pkl")

# ✅ Save feature columns — this was likely missing!
joblib.dump(X.columns.tolist(), "risk_features.pkl")

print("✅ Risk model and feature list saved in  folder.")

import joblib
model = joblib.load("risk_model.pkl")
features = joblib.load("risk_features.pkl")
print("✅ Loaded model and features:", features)
