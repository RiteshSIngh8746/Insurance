# InsureMate: Insurance Multi-Agent App 🛡️

InsureMate is a powerful Streamlit-based GenAI application designed to simplify and optimize insurance services through multiple intelligent agents. This end-to-end AI-powered solution is built for the modern insurance domain and is capable of assisting customers, field agents, and insurers alike.

The application combines traditional machine learning with generative AI to deliver intelligent insurance recommendations, risk profiling, fraud detection, and more — all through an interactive web-based UI.

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

* Python 3.8+
* Streamlit
* Google Generative AI Python SDK (`google-generativeai`)
* pandas
* joblib

Install dependencies:

```bash
pip install -r requirements.txt
```

---

  ⚙️ Setup Instructions

 1.  Clone the Repository 

```bash
git clone https://github.com/yourusername/insurance-multi-agent-app.git
cd insurance-multi-agent-app
```

 2.  Create Virtual Environment (Recommended) 

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

 3.  Place the Required Files 

Ensure the following files are present:

* `fraud_model.pkl`
* `feature_order.pkl`
* `agents/risk_model.pkl`
* `agents/risk_features.pkl`
* `style.css` (optional)

 4.  Set Your Google API Key 

Edit the `app.py` and replace the API key:

```python
try:
    genai.configure(api_key="YOUR_API_KEY")
except Exception as e:
    st.error("⚠️ We're currently experiencing issues with the AI services. Please contact Ritesh Singh (riteshsingh8746@gmail.com) for support.")
    st.stop()
```

> ✅ You may store the key in an environment variable and access it using `os.getenv("GOOGLE_API_KEY")` for security.

 5.  Run the Application 

```bash
streamlit run app.py
```

---

  🚀 Running the App

```bash
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

```bash
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

  🔐 API Key

To use the GenAI features, set your Google API key in the code:

```python
try:
    genai.configure(api_key="YOUR_API_KEY")
except Exception as e:
    st.error("⚠️ We're currently experiencing issues with the AI services. Please contact Ritesh Singh (riteshsingh8746@gmail.com) for support.")
    st.stop()
```

> ⚠️ Never expose real keys in production code or public repos. Use `.env` files or environment variables.

---

  📊 Project Explanation (Detailed)

 InsureMate is a full-stack AI-powered insurance ecosystem built with a modular and user-centric design. It integrates both predictive machine learning models and generative AI agents to cover major aspects of the insurance workflow, such as:

* ✅ Customer Onboarding: Collects essential user data through interactive forms to initiate the insurance process.
* ✅ Intelligent Plan Recommendation: Recommends best-fit plans from government and private insurers based on user profile.
* ✅ Claim Summary Generation: Generates professionally formatted summaries of incidents to assist with filing insurance claims.
* ✅ Fraud Detection: Uses an ML model to flag potentially fraudulent claims based on historical and contextual data.
* ✅ Risk Profiling: Evaluates user profiles using underwriting criteria to assign a low, moderate, or high-risk label.
* ✅ Field Agent Sales Training: Offers GenAI-powered coaching to improve sales techniques and objection handling for agents.
* ✅ Interactive Customer Support: Provides a chatbot interface to answer FAQs and complex insurance queries using Gemini.

 🎯 Key Components:

*  GenAI-Powered Reasoning : Uses Gemini to explain plan suggestions, respond to queries, and train field agents.
*  ML Models : Risk (`risk_model.pkl`) and fraud (`fraud_model.pkl`) models process structured data and return binary or multiclass predictions.
*  Streamlit UI : No complex setup — deployable with a single command. Easy input forms for different user journeys.
*  Modular Task Structure : Each agent serves a dedicated purpose, providing targeted assistance and reducing confusion.

 🧩 Real-world Application Use Cases:

* 🔍 Customers exploring insurance plans.
* 🧾 Claimants submitting reports and getting structured summaries.
* 🧠 Field agents needing quick sales training.
* 👨‍💻 Insurance analysts checking for fraud.
* 💬 Support agents automating repetitive queries.

 Tech Stack: 

* Frontend: Streamlit
* Backend: Python, ML models (pickle)
* LLM: Gemini via Google Generative AI SDK
* Styling: Custom CSS

 Scalability: 

* Modular agents can be extended for property insurance, auto, or micro-insurance domains.
* Integration-ready with any CRM or claim-processing backend.

---

  📌 License

This project is for educational and demonstration purposes. Modify and extend as needed for your own use case.

---

  🤝 Acknowledgements

Built by [Ritesh Singh](https://github.com/RiteshSIngh8746) as part of a GenAI Insurance Automation Project Hackathon for DSW Internship Drive
