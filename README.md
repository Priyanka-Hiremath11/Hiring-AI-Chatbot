TalentScout : AI Hiring Assistant (Streamlit & Groq AI)

Description:
The AI Hiring Assistant is an interactive web application designed to simulate a real-world technical interview experience. Built using Streamlit for the frontend and Groq AI (Llama 3) for natural language processing, the assistant guides candidates through a structured interview process, evaluates their technical knowledge, and provides instant feedback.

Key Features:

User-Friendly Interview Flow:
Sequentially collects candidate details, such as name, email, qualification, and key skills, with built-in validation for accurate data input.

Automated Technical Question Generation:
Generates customized technical interview questions based on the candidate’s listed skills using AI.

Interactive Answer Submission:
Candidates can answer each technical question in a dedicated text area, simulating a real interview environment.

AI-Powered Evaluation:
After submission, the assistant evaluates the candidate’s answers, provides concise feedback, and assigns a rating (Beginner / Intermediate / Strong) automatically using AI.

Restart & Session Management:
Allows candidates to restart the interview at any time without refreshing the browser, leveraging Streamlit session state for seamless flow control.

Clean and Polished UI:
Built with Streamlit containers, step indicators, info/warning boxes, and clear headers for a professional, user-friendly interface.

Tech Stack:

Frontend / Framework: Streamlit

AI / NLP: Groq AI (Llama 3)

Environment Management: Python, dotenv

Deployment Ready: Streamlit Cloud (with secure API key handling via secrets)

Use Case:
Ideal for HR tech platforms, interview practice tools, and educational purposes, allowing users to practice technical interviews or pre-screen candidates automatically with AI-generated questions and evaluations.
