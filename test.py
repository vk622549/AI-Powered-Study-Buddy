import google.generativeai as genai

API_KEY = "my api key"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content(
    "Write 5 lines about Machine Learning"
)

print(response.text)