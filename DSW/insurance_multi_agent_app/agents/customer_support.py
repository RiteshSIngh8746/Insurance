def chat_with_agent(query):
    prompt = (
        f"You are a knowledgeable and friendly insurance customer support agent.\n"
        f"Answer the following customer query in a clear, detailed, and helpful manner.\n"
        f"Break down technical terms, give examples, and offer useful suggestions.\n\n"
        f"Customer Query: \"{query}\"\n\n"
        f"Please structure your response as follows:\n"
        f"1. **Overview** – A concise answer to the question.\n"
        f"2. **Detailed Explanation** – Explain in simple terms, include relevant examples.\n"
        f"3. **Tips or Advice** – Share useful insights.\n"
        f"4. **Next Steps** – What the customer can do next."
    )

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,
                top_p=1,
                top_k=40,
                max_output_tokens=1024  # 👈 Increase this from default (~256) to get long replies
            )
        )
        return response.text

    except Exception as e:
        print(f"[Gemini Error] {str(e)}")
        return (
            "❌ Our AI support agent is currently unavailable.\n\n"
            "📞 **Contact Human Support:**\n"
            "- 📱 Call: 1800-123-INSURE\n"
            "- 📧 Email: support@insuregenie.ai\n\n"
            "✅ Available 24x7 for your help."
        )
