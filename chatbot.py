import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()
api_key = os.getenv("gemini_class")

if not api_key:
    st.error("API key not found. Check your .env file.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = api_key

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Brutal AI Career Advisor", page_icon="🔥")

st.title("🔥 Brutally Honest AI Career Advisor")
st.caption("No hype. No sugarcoating. Just real AI career advice.")

# -----------------------------
# System Prompt
# -----------------------------
system_prompt = """
You are a brutally honest AI Career Advisor for students who want to enter Artificial Intelligence and Generative AI.

Your personality:
- Direct.
- Realistic.
- Slightly tough, but not insulting.
- Zero sugarcoating.

Your mission:
- Expose skill gaps clearly.
- Correct unrealistic expectations.
- Explain industry competition honestly.
- Give practical, actionable advice.
- Push students toward disciplined learning.

Response structure:

💣 Reality Check:
(Give a direct truth about their situation or question.)

📊 Where You Stand:
(Briefly assess what level this goal requires.)

🛠 What You Actually Need:
(List specific skills, tools, or actions required.)

🚀 If You’re Serious:
(Concrete next steps — no vague advice.)

Rules:
- Do not demotivate, but do not comfort unnecessarily.
- Do not invent salaries, job openings, or statistics.
- If the student is unrealistic, explain why.
- Prioritize accuracy over encouragement.
- Keep responses concise but impactful.
"""

# -----------------------------
# Initialize Client Once
# -----------------------------
if "client" not in st.session_state:
    st.session_state.client = genai.Client()

client = st.session_state.client

# -----------------------------
# Create Chat Session Once
# -----------------------------
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.5,
            max_output_tokens=400,
        ),
    )

# -----------------------------
# Store Messages
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display Chat History
# -----------------------------
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(message)

# -----------------------------
# User Input
# -----------------------------
user_input = st.chat_input("Ask about AI careers... if you're ready for honesty.")

if user_input:
    # Show user message
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response safely
    try:
        response = st.session_state.chat_session.send_message(user_input)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Error: {e}"

    # Store bot response
    st.session_state.messages.append(("assistant", bot_reply))

    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

# -----------------------------
# Clear Chat Button
# -----------------------------
if st.sidebar.button("Reset Conversation"):
    st.session_state.messages = []
    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
        ),
    )
    st.rerun()
