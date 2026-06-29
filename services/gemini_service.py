import google.generativeai as genai
from config.config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text