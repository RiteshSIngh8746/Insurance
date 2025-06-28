import streamlit as st

def run():
    st.subheader("📄 Insurance Claim Assistant")
    doc_uploaded = st.checkbox("Upload documents (simulated)")
    injury_type = st.selectbox("Select Claim Type", ["Accident", "Health", "Travel", "Life"])

    if st.button("Validate Claim"):
        if doc_uploaded:
            st.success(f"✅ Claim for '{injury_type}' appears valid. Forwarding to processing.")
        else:
            st.warning("⚠️ Missing required documents!")
