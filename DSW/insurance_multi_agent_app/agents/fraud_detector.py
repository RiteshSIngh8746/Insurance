# predict_with_genai.py

import pandas as pd
import joblib
import openai

# 1. Load trained model and features
model = joblib.load('fraud_model.pkl')
model_columns = joblib.load('feature_order.pkl')

# 2. Set your OpenAI API Key
openai.api_key = "your_openai_api_key_here"  # Replace this

# 3. New data to predict
new_case = pd.DataFrame([{
    'customer_age': 42,
    'claim_amount': 85000,
    'policy_coverage': 90000,
    'monthly_income': 28000,
    'incident_type': 'Theft',
    'report_delay_days': 35,
    'doctor_certificate': 'Yes',
    'police_report': 'No',
    'months_after_policy': 10
}])

# 4. One-hot encode and align with training columns
new_case_encoded = pd.get_dummies(new_case)
new_case_encoded = new_case_encoded.reindex(columns=model_columns, fill_value=0)

# 5. Predict fraud
prediction = model.predict(new_case_encoded)[0]
probability = model.predict_proba(new_case_encoded)[0][1]

print(f"\n🔍 Prediction: {'FRAUD' if prediction == 'Yes' else 'Not Fraud'}")
print(f"Probability of Fraud: {probability:.2%}")

# 6. GenAI Explanation
prompt = f"""
A customer aged {new_case['customer_age'][0]} reported a {new_case['incident_type'][0]} claim of ₹{new_case['claim_amount'][0]}, 
{new_case['report_delay_days'][0]} days after the incident. 
Doctor certificate: {new_case['doctor_certificate'][0]}, Police report: {new_case['police_report'][0]}. 
Monthly income: ₹{new_case['monthly_income'][0]}. 
Policy was bought {new_case['months_after_policy'][0]} months ago. 
Should this claim be considered fraudulent? Explain with reasoning like an insurance investigator.
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an insurance fraud expert."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=250
)

print("\n🧠 GenAI Explanation:")
print(response['choices'][0]['message']['content'].strip())
