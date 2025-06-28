import streamlit as st
import google.generativeai as genai
import time

# ---------------- CONFIG ----------------
genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- PROMPT GENERATOR ----------------
def generate_plan_prompt(data):
    prompt = (
        f"Act like an expert insurance advisor.\n"
        f"Based on the following customer profile, recommend the best 3 insurance plans from major Indian insurers "
        f"like LIC, HDFC Life, ICICI Prudential, SBI Life, or government schemes. Include plan name, insurer, benefits, "
        f"claim settlement ratio (CSR) if possible, and explain why each plan fits:\n\n"
        f"Age: {data['age']}\n"
        f"Gender: {data['gender']}\n"
        f"Marital Status: {data['marital_status']}\n"
        f"Dependents: {data['dependents']}\n"
        f"Monthly Income: ₹{data['income']}\n"
        f"Occupation: {data['occupation']}\n"
        f"Health Conditions: {data['health']}\n"
        f"Smoker: {data['smoker']}\n"
        f"Alcohol Consumption: {data['alcohol']}\n"
        f"Financial Goal: {data['goal']}\n"
        f"Risk Appetite: {data['risk']}\n"
        f"Desired Coverage: ₹{data['coverage']}\n"
        f"Policy Duration: {data['duration']} years\n\n"
        f"Give details in simple bullet points under each plan. Mention key benefits and why it's suitable."
    )
    return prompt

# ---------------- RECOMMENDATION FUNCTION ----------------
def get_recommendation(user_data):
    try:
        prompt = generate_plan_prompt(user_data)
        response = model.generate_content(prompt)
        time.sleep(2)
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"

# ---------------- UI ----------------
st.set_page_config(page_title="SmartCover Advisor", layout="centered")
st.title("🛡️ SmartCover Advisor")
st.markdown("#### Get tailored insurance plan suggestions from trusted Indian insurers based on your profile")

with st.form("insurance_form"):
    st.markdown("### 👤 Personal Information")
    age = st.slider("Age", 18, 80)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married"])
    dependents = st.number_input("Number of Dependents", min_value=0)

    st.markdown("---")
    st.markdown("### 💼 Financial & Lifestyle Info")
    income = st.number_input("Monthly Income (₹)", min_value=5000, step=1000)
    occupation = st.text_input("Occupation", placeholder="e.g., Private Job, Business, Freelancer")
    health = st.selectbox("Any Health Conditions?", ["None", "Diabetic", "Hypertension", "Cardiac", "Other"])
    smoker = st.selectbox("Do you smoke?", ["No", "Yes"])
    alcohol = st.selectbox("Alcohol Consumption?", ["No", "Occasionally", "Regularly"])

    st.markdown("---")
    st.markdown("### 🎯 Goals & Policy Preferences")
    goal = st.selectbox("Primary Financial Goal", ["Family Protection", "Wealth Creation", "Retirement", "Child Education"])
    risk = st.selectbox("Risk Appetite", ["Low", "Moderate", "High"])
    coverage = st.number_input("Desired Coverage (₹)", min_value=100000, step=100000)
    duration = st.slider("Policy Duration (Years)", 5, 40)

    submitted = st.form_submit_button("🔍 Get Recommended Plans")

if submitted:
    with st.spinner("Analyzing your profile and searching best plans..."):
        user_data = {
            "age": age,
            "gender": gender,
            "marital_status": marital_status,
            "dependents": dependents,
            "income": income,
            "occupation": occupation,
            "health": health,
            "smoker": smoker,
            "alcohol": alcohol,
            "goal": goal,
            "risk": risk,
            "coverage": coverage,
            "duration": duration
        }

        recommendations = get_recommendation(user_data)
        st.markdown("## 🧠 Personalized Recommendations")
        st.write(recommendations)
