import streamlit as st
import google.generativeai as genai
import time
import pickle
import os
import pandas as pd

# ------------------ CONFIG ------------------
genai.configure(api_key="AIzaSyCrIlEoMuhKUn-TSfWxKMWTc-iTZxIe5QI")  # Replace with your valid Gemini API key
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------ HELPER FUNCTIONS ------------------
def explain_recommendation(age, gender, marital_status, dependents, income, occupation, health, smoker, alcohol, goal, risk, coverage, duration):
    prompt = (
        f"Act like an expert insurance advisor.\n"
        f"Recommend top 3 insurance plans from LIC, HDFC Life, SBI Life, ICICI Prudential, or government schemes.\n\n"
        f"Customer Profile:\n"
        f"Age: {age}\n"
        f"Gender: {gender}\n"
        f"Marital Status: {marital_status}\n"
        f"Dependents: {dependents}\n"
        f"Monthly Income: ₹{income}\n"
        f"Occupation: {occupation}\n"
        f"Health Conditions: {health}\n"
        f"Smoker: {smoker}\n"
        f"Alcohol Consumption: {alcohol}\n"
        f"Financial Goal: {goal}\n"
        f"Risk Appetite: {risk}\n"
        f"Coverage Desired: ₹{coverage}\n"
        f"Policy Duration: {duration} years\n\n"
        f"List top plans with benefits, insurer name, and claim settlement ratio (CSR) if available. Explain each plan's suitability."
    )
    try:
        response = model.generate_content(prompt)
        time.sleep(2)
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"

def predict_underwriting_risk(age, income, health, smoker, claim_history):
    try:
        import pandas as pd
        import joblib
        import os

        # Load model and features
        with open(os.path.join( "risk_model.pkl"), "rb") as f:
            model = joblib.load(f)
        with open(os.path.join( "risk_features.pkl"), "rb") as f:
            model_cols = joblib.load(f)

        df = pd.DataFrame([{
            "age": age,
            "income": income,
            "health": health,
            "smoker": smoker,
            "claim_history": claim_history
        }])

        df = pd.get_dummies(df)
        df = df.reindex(columns=model_cols, fill_value=0)

        return model.predict(df)[0]
    except Exception as e:
        return f"Error: {e}"
    
def detect_fraud(age, claim_amount, policy_coverage, income, incident_type, delay_days, doctor_cert, police_rep, months_since_policy):
    try:
        import pandas as pd
        import joblib
        import os

        # Load model and columns
        current_dir = os.path.dirname(__file__)
        with open(os.path.join( "fraud_model.pkl"), "rb") as f:
            model = joblib.load(f)
        with open(os.path.join("feature_order.pkl"), "rb") as f:
            model_columns = joblib.load(f)

        # Create input row
        input_df = pd.DataFrame([{
            'customer_age': age,
            'claim_amount': claim_amount,
            'policy_coverage': policy_coverage,
            'monthly_income': income,
            'incident_type': incident_type,
            'report_delay_days': delay_days,
            'doctor_certificate': doctor_cert,
            'police_report': police_rep,
            'months_after_policy': months_since_policy
        }])

        # One-hot encode and align
        input_df = pd.get_dummies(input_df)
        input_df = input_df.reindex(columns=model_columns, fill_value=0)

        # Predict
        return model.predict(input_df)[0]
    except Exception as e:
        return f"Error: {str(e)}"


def chat_with_agent(query):
    prompt = f"You are an insurance support agent. Answer the following question in a helpful, concise manner:\n\n{query}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

 # Internal function to predict risk
def predict_risk_level(age, income, health, smoker):
    try:
        import pandas as pd
        import joblib
        with open("agents/risk_model.pkl", "rb") as f:
            model = joblib.load(f)
        with open("agents/risk_features.pkl", "rb") as f:
            features = joblib.load(f)

        # 👇 claim_history hardcoded as "No"
        df = pd.DataFrame([{
            "age": age,
            "income": income,
            "health": health,
            "smoker": smoker,
            "claim_history": "No"
        }])

        df = pd.get_dummies(df)
        df = df.reindex(columns=features, fill_value=0)
        return model.predict(df)[0]
    except Exception as e:
        return f"Error: {e}"


# ------------------ Sidebar Navigatio

def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ `{file_name}` not found. Skipping custom styling.")

# Call the function with correct filename

current_dir = os.path.dirname(__file__)
local_css(os.path.join(current_dir, "style.css"))

st.markdown(
    """
    <div class="top-banner">
        <div>🤝 <b>InsureMate : Your Insurance Partner</b></div>
        <div style="font-size: 16px; font-weight: 400;">"Always with you for the right decision."</div>
    </div>
    """,
    unsafe_allow_html=True
)


option = st.sidebar.radio(
    "Choose Task",
    [
        "🧠 Insurance Recommendation",
        "🚨 Fraud Detection",
        "💬 Customer Support Chatbot",
        "🎓 Field Sales Training Agent",
        "🧾 Insurance Claim Assistant",
        "📌 Underwriting & Risk Assessment Agent" ,

        
        "🏢 About Insurance Companies",
        
    ]
)


if option == "🧠 Insurance Recommendation":
    st.subheader("🧠 Get Personalized Insurance Plan Recommendations")

    # Basic Profile
    age = st.slider("Age", 18, 80, 30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married"])
    dependents = st.number_input("Number of Dependents", min_value=0, value=1)
    income = st.number_input("Monthly Income (₹)", min_value=5000, step=1000)
    occupation = st.text_input("Occupation", placeholder="e.g., IT Professional, Shop Owner")
    health = st.selectbox("Health Condition", ["Healthy", "Diabetic", "Heart Patient", "Hypertension", "Other"])
    smoker = st.selectbox("Do you Smoke?", ["No", "Yes"])
    goal = st.selectbox(
        "Select Your Primary Insurance Goal",
        ["Family Protection", "Health Insurance", "Retirement Planning", "Wealth Creation", "Child Education", "Critical Illness Cover", "Accident or Disability", "Death Claim Benefit"]
    )
    risk = st.selectbox("Risk Appetite", ["Low", "Moderate", "High"])
    coverage = st.number_input("Expected Insurance Coverage (₹)", min_value=100000, step=50000, value=1000000)
    duration = st.slider("Policy Duration (Years)", 5, 40, value=20)

    if st.button("📋 Get AI-Based Recommendations"):
        with st.spinner("Consulting AI for personalized insurance advice..."):
            try:
                # STEP 1: Explain the goal strategy
                strategy_prompt = f"""
You are a certified insurance advisor.

Explain in 5–6 bullet points the best insurance strategies and plan types suited for the goal: "{goal}".
Also mention what kind of coverage and policy duration is usually suitable for this goal.
Be practical and India-focused.
"""
                strategy_response = model.generate_content(strategy_prompt)
                st.markdown("### 🎯 Strategy for Your Goal")
                st.write(strategy_response.text)

                # STEP 2: Get plan recommendations
                plan_prompt = f"""
Act as an expert financial and insurance advisor.

Based on the following user profile, recommend 4–5 **realistic insurance plans** (both government and private) specifically focused on the goal: "{goal}".
Return a table with these columns:

- Provider (e.g. LIC, ICICI, PMJJBY)
- Plan Name
- Type (e.g., Term, Health, Retirement)
- Annual Premium Estimate (₹)
- Coverage (₹)
- Key Features (1–2 lines)

User profile:
Age: {age}, Gender: {gender}, Marital Status: {marital_status}, Dependents: {dependents}, 
Income: ₹{income}/month, Occupation: {occupation}, Health: {health}, 
Smoker: {smoker}, Risk Profile: {risk}, Coverage Needed: ₹{coverage}, Duration: {duration} years.
"""
                plan_response = model.generate_content(plan_prompt)

                st.markdown("### 📊 Recommended Insurance Plans for Your Goal")
                st.markdown(plan_response.text)

                # Optional: Save log
                with open("recommendation_logs.csv", "a") as f:
                    f.write(f"{age},{income},{goal},{risk},{coverage},{duration}\n")

            except Exception as e:
                st.error(f"❌ AI Recommendation failed: {e}")


elif option == "📊 Risk Checker":
    st.subheader("Check Your Insurance Risk Level")

    age = st.slider("Age", 18, 70, 35)
    income = st.number_input("Monthly Income (₹)", min_value=1000, step=1000)
    dependents = st.number_input("Number of Dependents", min_value=0, step=1)
    expenses = st.number_input("Monthly Expenses (₹)", min_value=500, step=500)

    if st.button("🧠 Assess Risk"):
        with st.spinner("Evaluating underwriting risk..."):
            risk = predict_underwriting_risk(age, income, health, smoker, claim_history)
            st.markdown(f"### 📊 Risk Level: `{risk}`")

            try:
                reason_prompt = (
                    f"Explain why a {age}-year-old {health.lower()} {smoker.lower()} individual "
                    f"with ₹{income} monthly income and {'past' if claim_history == 'Yes' else 'no'} claims "
                    f"is categorized as '{risk}' risk for insurance underwriting."
                )
                explanation = model.generate_content(reason_prompt).text
                st.markdown("### 🧠 Explanation from GenAI")
                st.write(explanation)
            except Exception as e:
                st.warning(f"AI explanation failed: {e}")
# ------------------ Task: Fraud Detection ------------------
elif option == "🚨 Fraud Detection":
    st.subheader("Detect Fraudulent Claims")

    age = st.slider("Claimant's Age", 18, 80, 40)
    income = st.number_input("Monthly Income (₹)", min_value=1000, step=1000)
    claim_amount = st.number_input("Claim Amount (₹)", min_value=1000, step=1000)
    policy_coverage = st.number_input("Policy Coverage Amount (₹)", min_value=1000, step=1000)
    delay_days = st.slider("Days Delay in Reporting", 0, 60, 5)
    incident_type = st.selectbox("Incident Type", ["Theft", "Accident", "Fire"])
    doctor_cert = st.selectbox("Doctor Certificate Available?", ["Yes", "No"])
    police_rep = st.selectbox("Police Report Available?", ["Yes", "No"])
    months_since_policy = st.slider("Months After Policy Purchased", 0, 60, 12)

    if st.button("🔍 Check for Fraud"):
        with st.spinner("Analyzing claim..."):
            fraud = detect_fraud(
                age,
                claim_amount,
                policy_coverage,
                income,
                incident_type,
                delay_days,
                doctor_cert,
                police_rep,
                months_since_policy
            )
            if isinstance(fraud, str):
                st.error(fraud)
            else:
                result = "⚠️ Fraudulent Claim Detected!" if fraud == "Yes" else "✅ Claim Looks Genuine."
                st.markdown(f"### {result}")

# ------------------ Task: Customer Support Chatbot ------------------
# ------------------ Task: Customer Support Chatbot ------------------
elif option == "💬 Customer Support Chatbot":
    st.subheader("Chat with Insurance Support Assistant")

    st.markdown("### 📋 Frequently Asked Questions")

    faqs = {
        "What is term insurance?": "Term insurance is a type of life insurance that provides coverage for a fixed period of time. If the insured dies during the term, a death benefit is paid to the nominee.",
        "What does health insurance cover?": "Health insurance typically covers hospitalization, surgeries, doctor consultations, and in some cases, pre and post-hospitalization expenses.",
        "Can I have multiple insurance policies?": "Yes, you can have multiple insurance policies from different providers as long as you meet their eligibility criteria.",
        "How to file an insurance claim?": "To file a claim, you need to contact your insurer, fill the claim form, submit required documents (like bills, FIR, death certificate), and wait for verification.",
        "How is premium calculated?": "Premium is calculated based on your age, sum insured, policy duration, health conditions, and risk profile."
    }

    col1, col2 = st.columns(2)
    with col1:
        for q in list(faqs.keys())[:3]:
            if st.button(q):
                st.markdown(f"**Q:** {q}")
                st.markdown(f"**A:** {faqs[q]}")

    with col2:
        for q in list(faqs.keys())[3:]:
            if st.button(q):
                st.markdown(f"**Q:** {q}")
                st.markdown(f"**A:** {faqs[q]}")

    st.markdown("---")
    st.markdown("### 🧾 Ask a Custom Question")

    user_query = st.text_area("Type your insurance-related query here:")
    if st.button("💬 Ask"):
        with st.spinner("Getting response..."):
            answer = chat_with_agent(user_query)
            st.markdown("### 🤖 Support Response")
            st.write(answer)

# ------------------ Task: Field Sales Training Agent ------------------
elif option == "🎓 Field Sales Training Agent":
    st.subheader("Field Sales Training Assistant")

    st.markdown("💡 **Ask any question to train yourself on field insurance sales techniques.**")
    st.markdown("*Example questions:*")
    st.markdown("- How to pitch term insurance to a 35-year-old client?")
    st.markdown("- How do I handle objections about premium cost?")
    st.markdown("- What are the best tips to close insurance sales?")
    st.markdown("- How to explain insurance plans in simple terms?")

    user_training_query = st.text_area("Enter your sales training query:")

    if st.button("🎯 Train Me"):
        with st.spinner("Fetching sales training advice..."):
            prompt = (
                f"You are a professional field insurance sales trainer. "
                f"Give advice or techniques for the following situation:\n\n"
                f"{user_training_query}"
            )
            try:
                training_response = model.generate_content(prompt)
                st.markdown("### 🎓 Sales Training Response")
                st.write(training_response.text)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

elif option == "📌 Underwriting & Risk Assessment Agent":
    st.subheader("📌 Dynamic Underwriting & Risk Assessment")

    # Collect inputs
    age = st.slider("Applicant Age", 18, 80, 40)
    income = st.number_input("Monthly Income (₹)", min_value=5000, step=1000)
    health = st.selectbox("Health Condition", ["Healthy", "Diabetic", "Hypertension", "Both"])
    smoker = st.selectbox("Smoking Habit", ["Non-Smoker", "Smoker"])

   

    if st.button("🧠 Assess Underwriting Risk"):
        with st.spinner("Evaluating underwriting risk..."):
            risk_level = predict_risk_level(age, income, health, smoker)

            if isinstance(risk_level, str) and "Error" in risk_level:
                st.error(risk_level)
            else:
                st.success(f"🧠 Risk Level: `{risk_level}`")

                # GenAI explanation
                try:
                    prompt = (
                        f"Explain why a {age}-year-old individual who is a "
                        f"{health.lower()} {'smoker' if smoker == 'Smoker' else 'non-smoker'}, "
                        f"earning ₹{income} monthly, would be classified as '{risk_level}' underwriting risk."
                    )
                    explanation = model.generate_content(prompt)
                    st.markdown("### 📘 Underwriting Risk Explanation")
                    st.write(explanation.text)
                except Exception as e:
                    st.warning(f"GenAI explanation failed: {e}")


elif option == "🧾 Insurance Claim Assistant":
    st.subheader("Submit an Insurance Claim")

    # Input fields
    age = st.slider("Your Age", 18, 80, 35)
    income = st.number_input("Yearly Premium (₹)", min_value=1000, step=1000)
    claim_amount = st.number_input("Claim Amount (₹)", min_value=1000, step=1000)
    incident = st.text_area("Describe the Incident", help="Mention details like what happened, when, and where.")
    location = st.selectbox("Location of Incident", ["Urban", "Rural", "Semi-Urban"])
    location_encoded = 0 if location == "Urban" else 1 if location == "Semi-Urban" else 2
    file_upload = st.file_uploader("Upload Supporting Document(s) (optional)", type=["pdf", "jpg", "png", "jpeg"])

    if st.button("📝 Generate Claim Summary"):
        with st.spinner("Generating summary..."):
            prompt = (
                f"Generate a formal insurance claim summary for a {age}-year-old earning ₹{income} monthly, "
                f"claiming ₹{claim_amount} for the following incident:\n\n'{incident}'\n"
                f"Location: {location}. Include a professional tone, summary, and required documents."
            )
            try:
                response = model.generate_content(prompt)
                st.markdown("### 📄 Generated Claim Summary")
                st.write(response.text)

                # Save log (optional)
                with open("claim_logs.csv", "a") as f:
                    f.write(f"{age},{income},{claim_amount},{location},{incident[:50]}...\n")

                # Predict Risk & Fraud (optional)
                try:
                    risk = predict_risk(age, income, 0, income * 0.4)
                    fraud = detect_fraud(age, income, claim_amount, location_encoded)
                    st.markdown(f"**🔍 Risk Level:** `{risk}`")
                    st.markdown(f"**🚨 Fraud Prediction:** {'⚠️ Fraud' if fraud == 1 else '✅ Genuine'}")
                except Exception as e:
                    st.warning(f"Risk/Fraud model error: {e}")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                
elif option == "📈 Premium Calculator & Plan Advisor":
    st.subheader("📈 Premium Calculator & Plan Recommender")

    # User Inputs
    age = st.slider("Your Age", 18, 80, 35)
    income = st.number_input("Monthly Income (₹)", min_value=5000, step=1000)
    health = st.selectbox("Health Condition", ["Healthy", "Diabetic", "Hypertension", "Both"])
    smoker = st.selectbox("Smoking Habit", ["Non-Smoker", "Smoker"])
    coverage = st.number_input("Desired Coverage Amount (₹)", min_value=100000, step=50000, value=1000000)
    duration = st.slider("Policy Duration (in Years)", 5, 40, 20)
    policy_type = st.selectbox("Policy Type", ["Term", "Health", "Life"])

    # Predict risk using model, silently set claim_history = "No"
    def predict_risk_level(age, income, health, smoker):
        try:
            import pandas as pd
            import joblib
            with open("agents/risk_model.pkl", "rb") as f:
                model = joblib.load(f)
            with open("agents/risk_features.pkl", "rb") as f:
                features = joblib.load(f)
            df = pd.DataFrame([{
                "age": age,
                "income": income,
                "health": health,
                "smoker": smoker,
                "claim_history": "No"  # 👈 Fixed value, not shown to user
            }])
            df = pd.get_dummies(df)
            df = df.reindex(columns=features, fill_value=0)
            return model.predict(df)[0]
        except Exception as e:
            return f"Error: {e}"

    # Premium calculation based on risk level
    def calculate_premium(base_rate, age, duration, risk_level):
        multiplier = 1.0
        if risk_level == "Moderate":
            multiplier = 1.2
        elif risk_level == "High":
            multiplier = 1.5
        age_factor = 1 + ((age - 30) * 0.01)
        return int(base_rate * age_factor * multiplier * duration)

    # Run calculation
    if st.button("💰 Calculate Premium & Suggest Plan"):
        with st.spinner("Evaluating your profile..."):
            risk = predict_risk_level(age, income, health, smoker)

            if isinstance(risk, str) and "Error" in risk:
                st.error(risk)
            else:
                base_rate = coverage / 10000  # Simplified base rate
                premium = calculate_premium(base_rate, age, duration, risk)

                st.markdown(f"### 🧾 Estimated Annual Premium: ₹{premium:,}")
                st.markdown(f"**🧠 Risk Level:** `{risk}`")

                # Dummy plan data
                plans = [
                    {"name": "ShieldTerm", "premium": premium, "coverage": coverage, "csr": 99.1},
                    {"name": "LifeSure+", "premium": int(premium * 1.1), "coverage": coverage + 200000, "csr": 98.8},
                    {"name": "HealthPro Secure", "premium": int(premium * 0.95), "coverage": coverage - 100000, "csr": 97.5}
                ]

                st.markdown("### 📊 Comparison of Top Plans")
                st.table(pd.DataFrame(plans))

                # GenAI explanation
                try:
                    plan_str = ", ".join(
                        [f"{p['name']} (₹{p['premium']}/yr, ₹{p['coverage']} cover, CSR {p['csr']}%)" for p in plans]
                    )
                    prompt = (
                        f"Recommend the best insurance plan for a {age}-year-old earning ₹{income} monthly, "
                        f"with {health} health status, {'a smoker' if smoker == 'Smoker' else 'non-smoker'}, "
                        f"desiring ₹{coverage} cover for {duration} years. Options are: {plan_str}."
                    )
                    response = model.generate_content(prompt)
                    st.markdown("### 💡 Gemini Recommendation")
                    st.write(response.text)
                except Exception as e:
                    st.warning(f"GenAI explanation failed: {e}")

elif option == "🏢 About Insurance Companies":
    st.subheader("🏢 Insurance Providers in India")

    companies = {
        "LIC (Life Insurance Corporation of India)": {
            "Founded": "1956",
            "Headquarters": "Mumbai",
            "Popular Plans": ["Jeevan Anand", "Jeevan Labh", "Jeevan Shanti"],
            "About": "India’s largest government-owned insurance company with a trusted legacy. Known for endowment, term, and pension plans."
        },
        "HDFC Life": {
            "Founded": "2000",
            "Headquarters": "Mumbai",
            "Popular Plans": ["Click2Protect Life", "Sanchay Plus"],
            "About": "Leading private life insurer offering term, ULIP, and retirement plans. Strong claim settlement and digital experience."
        },
        "ICICI Prudential Life": {
            "Founded": "2001",
            "Headquarters": "Mumbai",
            "Popular Plans": ["iProtect Smart", "Guaranteed Pension Plan"],
            "About": "Among top private insurers. Known for innovation in term insurance and savings plans."
        },
        "SBI Life": {
            "Founded": "2001",
            "Headquarters": "Mumbai",
            "Popular Plans": ["Smart Shield", "Retire Smart"],
            "About": "Joint venture between SBI and BNP Paribas. Trusted for savings, retirement, and protection plans."
        },
        "Max Life Insurance": {
            "Founded": "2000",
            "Headquarters": "New Delhi",
            "Popular Plans": ["Smart Secure Plus", "Max Life Fast Track Super"],
            "About": "Customer-centric insurer known for long-term savings and protection plans."
        }
    }

    selected = st.selectbox("Select a Company", list(companies.keys()))

    info = companies[selected]
    st.markdown(f"### 🏢 {selected}")
    st.markdown(f"- **Founded:** {info['Founded']}")
    st.markdown(f"- **Headquarters:** {info['Headquarters']}")
    st.markdown(f"- **Popular Plans:** {', '.join(info['Popular Plans'])}")
    st.markdown(f"**📝 About:** {info['About']}")
