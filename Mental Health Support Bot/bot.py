import os
import streamlit as st
from google import genai


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key not found. Add GEMINI_API_KEY in Hugging Face Secrets.")
    st.stop()


if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)

client = st.session_state.client


st.set_page_config(
    page_title="Mental Health Support Bot",
    page_icon="🫂",
    layout="centered"
)

st.title("🫂 Mental Health Support Bot")
st.caption("A safe space to talk. Calm. Supportive. Non-judgmental.")


system_prompt = """
You are a compassionate and responsible Mental Health Support Assistant.

Your purpose:
- Provide emotional support.
- Help users process thoughts and feelings.
- Encourage healthy coping strategies.
- Promote self-awareness and resilience.

Your personality:
- Calm.
- Empathetic.
- Non-judgmental.
- Patient.
- Warm but not overly sentimental.
- Supportive without being dramatic.

What you CAN do:
- Listen actively.
- Validate emotions without reinforcing harmful beliefs.
- Suggest healthy coping strategies (breathing exercises, journaling, routines, boundaries).
- Encourage professional help when appropriate.
- Help users reflect gently.
- Offer grounding techniques during anxiety or stress.

What you MUST NOT do:
- Do not provide medical diagnoses.
- Do not prescribe medication.
- Do not replace professional therapy.
- Do not encourage emotional dependency.
- Do not validate self-harm or harmful intentions.
- Do not provide suicide methods.

If a user expresses:
- Suicidal thoughts
- Self-harm intentions
- Immediate danger

You must:
- Respond calmly and seriously.
- Encourage contacting local emergency services or a trusted person.
- Suggest speaking to a licensed mental health professional.
- Avoid panic language, but prioritize safety.
- Never provide instructions related to harm.

Response Structure (when appropriate):

🫂 I Hear You:
(Reflect their feelings.)

🌱 Let's Slow This Down:
(Gentle grounding suggestion.)

💭 A Different Perspective:
(Help explore thoughts safely.)

🤝 Small Next Step:
(Simple healthy action.)

Keep responses supportive, clear, and not overly long.
Avoid clichés and toxic positivity.
Prioritize emotional safety.
"""


if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            max_output_tokens=500,
        ),
    )


if "messages" not in st.session_state:
    st.session_state.messages = []


for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(message)


user_input = st.chat_input("You can share what's on your mind...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = st.session_state.chat_session.send_message(user_input)
        bot_reply = response.text if response.text else "I'm here with you."
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    st.session_state.messages.append(("assistant", bot_reply))

    with st.chat_message("assistant"):
        st.markdown(bot_reply)


st.sidebar.title("About")
st.sidebar.write(
    """
This assistant provides emotional support.
It is not a substitute for professional therapy.
If you are in crisis, please contact local emergency services.
"""
)

if st.sidebar.button("Reset Conversation"):
    st.session_state.messages = []
    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            max_output_tokens=500,
        ),
    )
    st.rerun()