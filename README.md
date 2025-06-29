InsureMate: Insurance Multi-Agent App 🛡️

InsureMate is a powerful Streamlit-based GenAI application designed to simplify and optimize insurance services through multiple intelligent agents. This app helps users with:

* Personalized insurance plan recommendations
* Fraudulent claim detection
* Customer support chatbot
* Field sales training assistance
* Risk & underwriting assessment
* Claim summary generation
* Company details exploration

---

🔧 Features

1. 🧠 Insurance Recommendation
AI-powered suggestions of insurance plans based on user profile (age, gender, income, goals, etc.).

2. 🚨 Fraud Detection
Detect fraudulent insurance claims using a trained ML model (`fraud_model.pkl`).

3. 💬 Customer Support Chatbot
Ask insurance-related questions via a Gemini-powered chatbot.

 4. 🎓 Field Sales Training Agent
Sales tips and suggestions for insurance field agents powered by GenAI.

5. 🧾 Insurance Claim Assistant
Generates professional claim summaries based on incident input.

6. 📌 Risk & Underwriting Assessment
Evaluates applicant risk using ML models (`risk_model.pkl`).

7. 🏢 Insurance Company Info
Explore details of top insurance providers like LIC, HDFC, SBI, ICICI, etc.

---

   🧪 Requirements

Python 3.8+
Streamlit
Google Generative AI Python SDK (`google-generativeai`)
pandas
joblib

Install dependencies:

```
pip install -r requirements.txt
```

---

⚙️ Setup Instructions

1.   Clone the Repository  

```
git clone https://github.com/yourusername/insurance-multi-agent-app.git
cd insurance-multi-agent-app
```

    2.   Create Virtual Environment (Recommended)  

``` 
python -m venv venv
source venv/bin/activate    On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

    3.   Place the Required Files  

Ensure the following files are present:

* `fraud_model.pkl`
* `feature_order.pkl`
* `agents/risk_model.pkl`
* `agents/risk_features.pkl`
* `style.css` (optional)



```python
try:
    genai.configure(api_key="YOUR_API_KEY")
except Exception as e:
    st.error("⚠️ We're currently experiencing issues with the AI services. Please contact Ritesh Singh (riteshsingh8746@gmail.com) for support.")
    st.stop()
```

> ✅ You may store the key in an environment variable and access it using `os.getenv("GOOGLE_API_KEY")` for security.

    4.   Run the Application  

``` 
streamlit run app.py
```

---

   🚀 Running the App

``` 
streamlit run app.py
```

Ensure the following files are in place:

* `fraud_model.pkl`
* `feature_order.pkl`
* `risk_model.pkl` (inside `agents/` folder)
* `risk_features.pkl` (inside `agents/` folder)
* `style.css` (optional custom styling)

---

   📁 Project Structure

``` 
insurance_multi_agent_app/
├── app.py
├── fraud_model.pkl
├── feature_order.pkl
├── agents/
│   ├── risk_model.pkl
│   └── risk_features.pkl
├── style.css
├── recommendation_logs.csv (auto-generated)
├── claim_logs.csv (auto-generated)
```

---



   📌 License

This project is for educational and demonstration purposes. Modify and extend as needed for your own use case.

---

   🤝 Acknowledgements

Built by [Ritesh Singh](https://github.com/RiteshSIngh8746) as part of a GenAI Insurance Automation Project Hackathon for DSW Internship Drive
