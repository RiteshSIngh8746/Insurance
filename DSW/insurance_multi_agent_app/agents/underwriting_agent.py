import streamlit as st
import joblib
import numpy as np
import os

def run():
    st.subheader("⚖️ Risk Assessment Agent (ML Enabled)")

    age = st.slider("Age", 18, 80, 30)
    health = st.multiselect("Health Conditions", ["Diabetes", "None"])
    is_smoker = st.checkbox("Smoker?")
    occupation = st.selectbox("Occupation Risk", ["Low", "Medium", "High"])

    # Encode
    has_diabetes = 1 if "Diabetes" in health else 0
    smoker = int(is_smoker)
    occ_map = {"Low": 0, "Medium": 1, "High": 2}
    occ_risk = occ_map[occupation]

    if st.button("Predict Risk Score"):
        model_path = "risk_model.pkl"
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            features = np.array([[age, has_diabetes, smoker, occ_risk]])
            score = model.predict(features)[0]

            if score > 120:
                st.error(f"⚠️ High Risk: Score {score:.2f}")
            elif score > 80:
                st.warning(f"🟠 Medium Risk: Score {score:.2f}")
            else:
                st.success(f"✅ Low Risk: Score {score:.2f}")
        else:
            st.warning("Risk model not found. Train it using risk_model.py")
