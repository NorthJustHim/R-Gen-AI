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
users_db = {"test@example.com": "1234"}  # demo account

# -------------------------------
# Session State
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "first_visit" not in st.session_state:
    st.session_state.first_visit = datetime.datetime.now()

# -------------------------------
# Streamlit page config
# -------------------------------
st.set_page_config(page_title="✨ R-Gen AI", page_icon="⚡", layout="wide")

# Title and logo
col1, col2 = st.columns([6, 2])
with col1:
    st.markdown("<h1>✨ R-Gen AI 🚀</h1>", unsafe_allow_html=True)
with col2:
    st.image("https://img.icons8.com/fluency/48/rocket.png", width=40)

st.write("Your AI sidekick for hustles 🚀")

# -------------------------------
# Auth Section (top right corner)
# -------------------------------
colA, colB = st.columns([6, 2])
with colB:
    if not st.session_state.logged_in:
        st.markdown("### 🔐 Sign Up / Log In")
        option = st.radio("Choose:", ["Login", "Sign Up"], key="auth_radio")
        email = st.text_input("Email", key="auth_email")
        password = st.text_input("Password", type="password", key="auth_password")

        if option == "Sign Up":
            if st.button("Sign Up", key="signup_btn"):
                if email in users_db:
                    st.error("⚠️ Email already registered.")
                else:
                    users_db[email] = password
                    st.success("✅ Account created! Please log in.")

        elif option == "Login":
            if st.button("Login", key="login_btn"):
                if email in users_db and users_db[email] == password:
                    st.session_state.logged_in = True
                    st.success("✅ Logged in successfully!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Invalid email or password.")

    else:
        st.success("✅ Logged in!")
        if st.button("Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.experimental_rerun()

# -------------------------------
# Chatbot Section
# -------------------------------
# Check free trial (4 days)
days_passed = (datetime.datetime.now() - st.session_state.first_visit).days
trial_expired = days_passed >= 4 and not st.session_state.logged_in

if trial_expired:
    st.warning("⚠️ Free trial expired! Please log in or sign up to continue.")
else:
    st.subheader("Chat with R-Gen AI 🤖")

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






