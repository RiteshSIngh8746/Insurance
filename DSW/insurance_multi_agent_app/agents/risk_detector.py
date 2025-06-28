import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# -------- Step 1: Create dummy dataset --------
np.random.seed(42)

data = {
    "age": np.random.randint(18, 70, 100),
    "income": np.random.randint(20000, 100000, 100),
    "dependents": np.random.randint(0, 5, 100),
    "expenses": np.random.randint(5000, 70000, 100),
}

df = pd.DataFrame(data)

# Simulate risk: high if (expenses/income) > 0.7 or too many dependents
df["risk"] = np.where((df["expenses"]/df["income"] > 0.7) | (df["dependents"] > 3), "High",
              np.where((df["expenses"]/df["income"] < 0.4), "Low", "Moderate"))

# Encode labels
df["risk"] = df["risk"].map({"Low": 0, "Moderate": 1, "High": 2})

# -------- Step 2: Train the model --------
X = df[["age", "income", "dependents", "expenses"]]
y = df["risk"]

model = RandomForestClassifier()
model.fit(X, y)

# -------- Step 3: Save the model --------
save_path = os.path.join("agents", "fraud_model.pkl")
os.makedirs("agents", exist_ok=True)

with open(save_path, "wb") as f:
    pickle.dump(model, f)

print("✅ risk_model.pkl saved at:", save_path)
