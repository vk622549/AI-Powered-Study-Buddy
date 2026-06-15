import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")

# Page Config
st.set_page_config(
    page_title="AI Study Buddy Pro",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Buddy Pro")
st.write("Generate Notes, Summaries, Explanations and Quiz Questions using Gemini AI")

# Sidebar
st.sidebar.header("Options")
study_type = st.sidebar.selectbox(
    "Select Task",
    [
        "Generate Notes",
        "Explain Topic",
        "Create Quiz",
        "Summarize Text"
    ]
)

# User Input
user_input = st.text_area(
    "Enter Topic or Text",
    height=200
)

# Generate Button
if st.button("Generate Study Material"):

    if user_input.strip() == "":
        st.warning("Please enter a topic or text.")
    else:

        if study_type == "Generate Notes":
            prompt = f"""
            Create detailed study notes on:
            {user_input}
            """

        elif study_type == "Explain Topic":
            prompt = f"""
            Explain this topic in simple language:
            {user_input}
            """

        elif study_type == "Create Quiz":
            prompt = f"""
            Create 10 MCQ quiz questions with answers on:
            {user_input}
            """

        elif study_type == "Summarize Text":
            prompt = f"""
            Summarize the following text:
            {user_input}
            """

        try:
            response = model.generate_content(prompt)

            st.success("Generated Successfully ✅")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")