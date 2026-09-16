import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import PyPDF2
from datetime import datetime


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Study Buddy Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
# 3. GEMINI CONFIGURATION
# =========================================================

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None


# =========================================================
# 4. SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "history" not in st.session_state:
    st.session_state.history = []

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0

if "topics_studied" not in st.session_state:
    st.session_state.topics_studied = 0


# =========================================================
# 5. CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .feature-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,0.3);
        margin-bottom: 15px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 6. LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="main-title">🎓 AI Study Buddy Pro</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Your AI-Powered Learning Assistant</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("🔐 Student Login")

        name = st.text_input(
            "Enter your name"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if name.strip():

                st.session_state.logged_in = True
                st.session_state.user_name = name

                st.rerun()

            else:

                st.warning(
                    "Please enter your name."
                )

    st.stop()


# =========================================================
# 7. SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 AI Study Buddy")

    st.write(
        f"Welcome, **{st.session_state.user_name}**"
    )

    st.divider()

    menu = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📚 Generate Notes",
            "💡 Explain Topic",
            "📄 Summarize Text",
            "📝 Create Quiz",
            "📂 PDF Analyzer",
            "💬 Ask AI",
            "📊 Progress",
            "📜 Study History"
        ]
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.rerun()


# =========================================================
# 8. API CHECK
# =========================================================

if client is None:

    st.error(
        "Gemini API key not found. "
        "Please add GEMINI_API_KEY in your .env file."
    )

    st.stop()


# =========================================================
# 9. HELPER FUNCTION
# =========================================================

def generate_ai_response(prompt):

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Error: {str(e)}"


# =========================================================
# 10. SAVE HISTORY
# =========================================================

def save_history(feature, topic):

    st.session_state.history.append(
        {
            "feature": feature,
            "topic": topic,
            "time": datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            )
        }
    )


# =========================================================
# 11. DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">AI Study Buddy Pro</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Learn Smarter • Learn Faster'
        '</div>',
        unsafe_allow_html=True
    )

    st.header("📊 Your Study Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📚 Topics Studied",
            st.session_state.topics_studied
        )

    with col2:

        st.metric(
            "📝 Quizzes Taken",
            st.session_state.quiz_total // 10
        )

    with col3:

        if st.session_state.quiz_total > 0:

            percentage = (
                st.session_state.quiz_score
                / st.session_state.quiz_total
            ) * 100

            percentage = round(
                percentage,
                1
            )

        else:

            percentage = 0

        st.metric(
            "🎯 Average Score",
            f"{percentage}%"
        )

    st.divider()

    st.subheader("✨ Learning Tools")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="feature-card">

            ### 📚 Generate Notes

            Create structured AI-generated
            study notes from any topic.

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="feature-card">

            ### 📄 PDF Analyzer

            Upload study material and let AI
            analyze and summarize it.

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">

            ### 💡 Explain Topic

            Get simple explanations for
            difficult academic concepts.

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="feature-card">

            ### 📝 Create Quiz

            Generate MCQs to test your
            understanding.

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 12. GENERATE NOTES
# =========================================================

elif menu == "📚 Generate Notes":

    st.header("📚 AI Notes Generator")

    topic = st.text_input(
        "Enter topic",
        placeholder="Example: Machine Learning"
    )

    difficulty = st.selectbox(
        "Select Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    language = st.selectbox(
        "Language",
        [
            "English",
            "Hindi",
            "Hinglish"
        ]
    )

    if st.button(
        "✨ Generate Notes",
        use_container_width=True
    ):

        if topic.strip():

            prompt = f"""
            Create detailed study notes on:

            Topic: {topic}
            Level: {difficulty}
            Language: {language}

            Include:

            1. Definition
            2. Key concepts
            3. Important points
            4. Examples
            5. Advantages
            6. Disadvantages
            7. Applications
            8. Short conclusion

            Make the content student-friendly.
            """

            with st.spinner(
                "AI is preparing your notes..."
            ):

                result = generate_ai_response(
                    prompt
                )

            st.session_state.topics_studied += 1

            save_history(
                "Generate Notes",
                topic
            )

            st.subheader("📖 Generated Notes")

            st.markdown(result)

            st.download_button(
                "⬇️ Download Notes",
                data=result,
                file_name=f"{topic}_notes.txt"
            )

        else:

            st.warning(
                "Please enter a topic."
            )


# =========================================================
# 13. EXPLAIN TOPIC
# =========================================================

elif menu == "💡 Explain Topic":

    st.header("💡 AI Topic Explainer")

    topic = st.text_input(
        "What do you want to understand?",
        placeholder="Example: Neural Networks"
    )

    level = st.selectbox(
        "Explanation Level",
        [
            "Very Simple",
            "Beginner",
            "Detailed"
        ]
    )

    if st.button(
        "💡 Explain",
        use_container_width=True
    ):

        if topic.strip():

            prompt = f"""
            Explain the following topic:

            {topic}

            Explanation level:
            {level}

            Explain in simple student-friendly
            language.

            Include:
            - Definition
            - Simple explanation
            - Example
            - Real-world application
            - Key points
            """

            with st.spinner(
                "Preparing explanation..."
            ):

                result = generate_ai_response(
                    prompt
                )

            st.session_state.topics_studied += 1

            save_history(
                "Explain Topic",
                topic
            )

            st.subheader("🧠 Explanation")

            st.markdown(result)

        else:

            st.warning(
                "Please enter a topic."
            )


# =========================================================
# 14. SUMMARIZE TEXT
# =========================================================

elif menu == "📄 Summarize Text":

    st.header("📄 AI Text Summarizer")

    text = st.text_area(
        "Paste your study material",
        height=250
    )

    summary_type = st.selectbox(
        "Summary Type",
        [
            "Short Summary",
            "Detailed Summary",
            "Exam-Oriented Summary"
        ]
    )

    if st.button(
        "✨ Summarize",
        use_container_width=True
    ):

        if text.strip():

            prompt = f"""
            Summarize the following study material.

            Summary type:
            {summary_type}

            Make it clear and useful for students.

            Text:
            {text}
            """

            with st.spinner(
                "Creating summary..."
            ):

                result = generate_ai_response(
                    prompt
                )

            save_history(
                "Summarize Text",
                "User Text"
            )

            st.subheader("📋 Summary")

            st.markdown(result)

            st.download_button(
                "⬇️ Download Summary",
                data=result,
                file_name="summary.txt"
            )

        else:

            st.warning(
                "Please enter some text."
            )


# =========================================================
# 15. CREATE QUIZ
# =========================================================

elif menu == "📝 Create Quiz":

    st.header("📝 AI Quiz Generator")

    topic = st.text_input(
        "Enter quiz topic",
        placeholder="Example: Python Programming"
    )

    number = st.selectbox(
        "Number of Questions",
        [5, 10, 15]
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    if st.button(
        "📝 Generate Quiz",
        use_container_width=True
    ):

        if topic.strip():

            prompt = f"""
            Create {number} multiple-choice questions
            on {topic}.

            Difficulty: {difficulty}

            Format each question like:

            Q1. Question?

            A. Option
            B. Option
            C. Option
            D. Option

            Answer: A

            Explanation:
            Explain why the answer is correct.
            """

            with st.spinner(
                "Generating quiz..."
            ):

                result = generate_ai_response(
                    prompt
                )

            save_history(
                "Create Quiz",
                topic
            )

            st.session_state.quiz_total += number

            st.subheader("📝 Generated Quiz")

            st.markdown(result)

            st.download_button(
                "⬇️ Download Quiz",
                data=result,
                file_name=f"{topic}_quiz.txt"
            )

        else:

            st.warning(
                "Please enter a topic."
            )


# =========================================================
# 16. PDF ANALYZER
# =========================================================

elif menu == "📂 PDF Analyzer":

    st.header("📂 AI PDF Analyzer")

    uploaded_file = st.file_uploader(
        "Upload your study PDF",
        type=["pdf"]
    )

    option = st.selectbox(
        "What should AI generate?",
        [
            "Summary",
            "Detailed Notes",
            "Important Questions",
            "MCQs"
        ]
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        if st.button(
            "🤖 Analyze PDF",
            use_container_width=True
        ):

            try:

                reader = PyPDF2.PdfReader(
                    uploaded_file
                )

                pdf_text = ""

                for page in reader.pages:

                    page_text = page.extract_text()

                    if page_text:
                        pdf_text += page_text

                if not pdf_text.strip():

                    st.error(
                        "Could not extract text from PDF."
                    )

                else:

                    prompt = f"""
                    Analyze the following study material.

                    User wants:
                    {option}

                    Make the output useful for
                    college students.

                    Study Material:
                    {pdf_text[:30000]}
                    """

                    with st.spinner(
                        "AI is analyzing your PDF..."
                    ):

                        result = generate_ai_response(
                            prompt
                        )

                    save_history(
                        "PDF Analyzer",
                        uploaded_file.name
                    )

                    st.subheader(
                        f"📖 {option}"
                    )

                    st.markdown(result)

                    st.download_button(
                        "⬇️ Download Result",
                        data=result,
                        file_name="pdf_analysis.txt"
                    )

            except Exception as e:

                st.error(
                    f"PDF Error: {str(e)}"
                )


# =========================================================
# 17. ASK AI
# =========================================================

elif menu == "💬 Ask AI":

    st.header("💬 AI Doubt Solver")

    question = st.text_area(
        "Ask your academic question",
        placeholder="Example: Explain overfitting in Machine Learning.",
        height=150
    )

    if st.button(
        "🤖 Ask AI",
        use_container_width=True
    ):

        if question.strip():

            prompt = f"""
            You are an AI academic assistant.

            Answer this student's question:

            {question}

            Explain clearly and simply.
            Give examples where useful.
            """

            with st.spinner(
                "AI is thinking..."
            ):

                result = generate_ai_response(
                    prompt
                )

            save_history(
                "AI Doubt Solver",
                question[:50]
            )

            st.subheader(
                "🤖 AI Answer"
            )

            st.markdown(result)

        else:

            st.warning(
                "Please enter a question."
            )


# =========================================================
# 18. PROGRESS
# =========================================================

elif menu == "📊 Progress":

    st.header("📊 Learning Progress")

    total_questions = (
        st.session_state.quiz_total
    )

    correct = (
        st.session_state.quiz_score
    )

    if total_questions > 0:

        percentage = (
            correct / total_questions
        ) * 100

    else:

        percentage = 0

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Topics Studied",
            st.session_state.topics_studied
        )

    with col2:

        st.metric(
            "Quiz Questions",
            total_questions
        )

    with col3:

        st.metric(
            "Correct Answers",
            correct
        )

    st.divider()

    st.subheader(
        "📈 Overall Performance"
    )

    st.progress(
        min(percentage / 100, 1.0)
    )

    st.write(
        f"Current Score: {percentage:.1f}%"
    )


# =========================================================
# 19. STUDY HISTORY
# =========================================================

elif menu == "📜 Study History":

    st.header("📜 Study History")

    if st.session_state.history:

        for item in reversed(
            st.session_state.history
        ):

            st.write(
                f"**{item['feature']}**"
            )

            st.write(
                f"Topic: {item['topic']}"
            )

            st.caption(
                item["time"]
            )

            st.divider()

    else:

        st.info(
            "No study activity yet."
        )