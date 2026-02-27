import streamlit as st
import os
import re
from groq import Groq
from dotenv import load_dotenv

st.set_page_config(page_title="AI Hiring Assistant", page_icon="🤖")
st.title("🤖 AI Hiring Assistant")

# ---------------- LOAD API KEY (ENV + DEPLOY SAFE) ----------------
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# If not in .env, try Streamlit secrets (for deployment)
if not api_key and "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]

if not api_key:
    st.error("GROQ_API_KEY not found. Add it in .env or Streamlit secrets.")
    st.stop()

client = Groq(api_key=api_key)

# ---------------- QUESTIONS ----------------

questions = [
    "Hello! I'm your AI Hiring Assistant. I'll ask you a few questions to understand your background and skills, then generate some technical questions based on your input. Let's get started! Are You Ready? 🚀",
    "What is your full name?",
    "Enter your email address:",
    "What is your highest qualification?",
    "List your key skills:",
]

# ---------------- SESSION STATE ----------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.tech_questions = []
    st.session_state.tech_answers = []

# ---------------- EMAIL VALIDATION ----------------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# ---------------- BASIC QUESTIONS FLOW ----------------
if st.session_state.step < len(questions):

    question = questions[st.session_state.step]
    user_input = st.text_input(question, key=f"input_{st.session_state.step}")

    if st.button("Next"):
        if not user_input.strip() or user_input.lower() in ["i don't know", "idk", "not sure"]:
            st.warning("Please provide a valid answer")
        elif "email" in question.lower() and not is_valid_email(user_input):
            st.warning("Invalid email format")
        else:
            st.session_state.answers[question] = user_input
            st.session_state.step += 1
            st.rerun()

# ---------------- GENERATE TECH QUESTIONS ----------------
elif not st.session_state.tech_questions:

    with st.spinner("Generating technical questions..."):
        skills = st.session_state.answers["List your key skills:"]

        prompt = f"""
        Based on these skills: {skills}
        Generate exactly 5 technical interview questions.
        Return each question on a new line only.
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )

            q_list = response.choices[0].message.content.split("\n")
            st.session_state.tech_questions = [q.strip() for q in q_list if q.strip()][1:5]

        except Exception as e:
            st.error(f"Error generating questions: {e}")
            st.stop()

    st.rerun()

# ---------------- ASK TECH QUESTIONS ----------------
elif len(st.session_state.tech_answers) < len(st.session_state.tech_questions):

    idx = len(st.session_state.tech_answers)
    question = st.session_state.tech_questions[idx]

    user_input = st.text_area(question, key=f"tech_{idx}")

    if st.button("Submit Answer"):
        if not user_input.strip():
            st.warning("Please answer the question")
        else:
            st.session_state.tech_answers.append(user_input)
            st.rerun()
            st.chat_message("assistant").write(
            "Thanks! Our team will review your responses. Have a great day 🚀"
    )  


# ---------------- FINAL EVALUATION ----------------
else:
    
    st.success("Evaluation complete! See results below.")


    prompt = f"""
    Candidate Details:
    {st.session_state.answers}

    Technical Questions:
    {st.session_state.tech_questions}

    Candidate Answers:
    {st.session_state.tech_answers}

    Evaluate the candidate.
    Provide:
    1. Display Candidate details in proper table.
    2. list all Technical questions asked and all candidate answers clearly readable format.
    3. Short feedback.
    4. Rating: Beginner / Intermediate / Strong.
    """


    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        st.write("### 🧠 Evaluation Result")
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Error during evaluation: {e}")

# ---------------- RESTART BUTTON ----------------
st.divider()

if st.button("🔄 Restart Interview"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()



