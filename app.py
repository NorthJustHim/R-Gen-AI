import streamlit as st
import time
import google.generativeai as genai
import datetime

# -------------------------------
# Configure Gemini AI
# -------------------------------
genai.configure(api_key="AIzaSyBrIzyi5AGaQZ5CXVBQPVjZmiM7hCjoZpc")  # replace with your key
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------------
# Fake user database (demo only)
# -------------------------------
users_db = {
    "test@example.com": "1234"  # demo account
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# Track when user first visited (trial start date)
if "trial_start" not in st.session_state:
    st.session_state.trial_start = datetime.date.today()

# -------------------------------
# Streamlit page config
# -------------------------------
st.set_page_config(page_title="✨ R-Gen AI", page_icon="⚡", layout="wide")

# Title
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1 style="margin: 0;">✨ R-Gen AI</h1>
        <img src="https://img.icons8.com/fluency/48/rocket.png" width="40">
    </div>
    """,
    unsafe_allow_html=True
)
st.write("Your AI sidekick for hustles 🚀")

# -------------------------------
# Auth Section (top right corner)
# -------------------------------
with st.container():
    st.markdown(
        """
        <style>
            .auth-box {
                position: absolute;
                top: 20px;
                right: 30px;
                background: #f9f9f9;
                padding: 15px;
                border-radius: 12px;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
                width: 260px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)

        if not st.session_state.logged_in:
            st.markdown("### 🔑 Login / Sign Up")
            option = st.radio("Choose:", ["Login", "Sign Up"])
            email = st.text_input("Email", key="auth_email")
            password = st.text_input("Password", type="password", key="auth_pass")

            if option == "Sign Up":
                if st.button("Sign Up"):
                    if email in users_db:
                        st.error("⚠️ Email already registered.")
                    else:
                        users_db[email] = password
                        st.success("✅ Account created! Please log in.")

            elif option == "Login":
                if st.button("Login"):
                    if email in users_db and users_db[email] == password:
                        st.session_state.logged_in = True
                        st.success("✅ Logged in successfully!")
                        st.experimental_rerun()
                    else:
                        st.error("❌ Invalid email or password.")

        else:
            st.markdown("✅ Logged in")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.experimental_rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Trial check
# -------------------------------
trial_days = (datetime.date.today() - st.session_state.trial_start).days
trial_limit = 4
trial_over = (trial_days >= trial_limit) and not st.session_state.logged_in

# -------------------------------
# Chatbot Section
# -------------------------------
st.subheader("Chat with R-Gen AI 🤖")

if trial_over:
    st.warning("⚠️ Your 4-day free trial has ended. Please log in or sign up to continue.")
else:
    # Display past messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        # Wavy dots animation
        placeholder = st.empty()
        wave = ["·    ", " ·   ", "  ·  ", "   · ", "  ·  ", " ·   "]
        for i in range(12):
            placeholder.markdown(f"**{wave[i % len(wave)]}**")
            time.sleep(0.2)

        # Build AI prompt
        conversation_text = (
            "You are R-Gen AI, a helpful assistant. "
            "Correct spelling/grammar if needed and answer clearly. "
            "Do NOT repeat the user’s question.\n\n"
            f"User: {prompt}"
        )

        # AI response
        response = model.generate_content(conversation_text)
        bot_message = response.text

        # Replace dots with AI response
        placeholder.markdown(bot_message)
        st.session_state.messages.append({"role": "assistant", "content": bot_message})







