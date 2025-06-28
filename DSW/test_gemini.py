import google.generativeai as genai

genai.configure(api_key="AIzaSyCrIlEoMuhKUn-TSfWxKMWTc-iTZxIe5QI")  # Paste your working key

model = genai.GenerativeModel("models/gemini-1.5-flash")

response = model.generate_content("Say hello to Ritesh Singh!")
print(response.text)
