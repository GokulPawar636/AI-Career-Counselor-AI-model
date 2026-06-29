import google.generativeai as genai
from config.config import GOOGLE_API_KEY

print("Loading Gemini...")

print("API KEY:", GOOGLE_API_KEY[:10] if GOOGLE_API_KEY else "None")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash-lite")

def ask_gemini(prompt):

    print("Prompt length:", len(prompt))

    try:
        print("Sending request...")

        response = model.generate_content(prompt)

        print("Response received")

        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        raise
