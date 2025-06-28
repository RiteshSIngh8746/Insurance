import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def evaluate_pitch(pitch):
    prompt = f"""
    Evaluate the following insurance sales pitch for clarity, persuasion, and completeness. Provide feedback in 3 bullet points:\n\n{pitch}
    """
    response = model.generate_content(prompt)
    return response.text

def run():
    st.subheader("🎯 Field Sales Training Agent")

    pitch = st.text_area("Write or paste your insurance sales pitch")

    if st.button("Evaluate Pitch"):
        if pitch:
            feedback = evaluate_pitch(pitch)
            st.markdown("### 🧠 Gemini Feedback")
            st.markdown(feedback)
        else:
            st.warning("Please enter your pitch first.")
