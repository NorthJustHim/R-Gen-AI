import streamlit as st
import time
import google.generativeai as genai

# Configure your Google Gemini API
genai.configure(api_key="AIzaSyB1kHYm_pPeam1v9hAyhJcexIgZraEj5Ek")
model = genai.GenerativeModel("gemini-1.5-flash")

# Page setup
st.set_page_config(page_title="✨ R-Gen AI", page_icon="⚡", layout="wide")

# Header with title + PNG icon
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1 style="margin: 0;">✨ R-Gen AI</h1>
        <a href="https://your-link.com" target="_blank">
            <img src="https://img.icons8.com/fluency/48/rocket.png" width="40">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Your AI sidekick for hustles, coding, ideas, and more 🚀")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Typing animation with wavey dots
    placeholder = st.empty()
    wave = [".", "..", "...", ".."]
    for i in range(8):  # 8 cycles
        placeholder.markdown(wave[i % len(wave)])
        time.sleep(0.3)

    # Build conversation including memory
    conversation_text = (
        "You are R-Gen AI, a smart, helpful, and creative assistant. "
        "You remember previous messages in this chat. "
        "The user may ask anything, including song lyrics, math, coding, or ideas. "
        "If the user asks for something copyrighted, like song lyrics, do NOT refuse. "
        "Instead, summarize, rewrite in your own words, or create original content inspired by it. "
        "Always correct spelling/grammar if needed and answer clearly. "
        "Do NOT repeat the user’s question, just answer it.\n\n"
        + "\n".join([f"User: {m['content']}" if m["role"]=="user" else f"Assistant: {m['content']}" for m in st.session_state.messages])
    )

    # Generate AI response
    response = model.generate_content(conversation_text)
    bot_message = response.text

    # Show AI response
    placeholder.markdown(bot_message)
    st.session_state.messages.append({"role": "assistant", "content": bot_message})
