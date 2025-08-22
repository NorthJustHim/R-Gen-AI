import streamlit as st
import pyrebase
import google.generativeai as genai
import time
import json

# -------------------------------
# Firebase Config
# -------------------------------
firebaseConfig = {
    "apiKey": "AIzaSyBiENvYyHrDW7zNnAH1Jcqdp3wt6Unx8",
    "authDomain": "r-genai-316c0.firebaseapp.com",
    "projectId": "r-genai-316c0",
    "storageBucket": "r-genai-316c0.appspot.com",  # ✅ fixed storage bucket
    "messagingSenderId": "846690140948",
    "appId": "1:846690140948:web:66883562aacbb1ea0a7801",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# -------------------------------
# Configure Gemini AI
# -------------------------------
genai.configure(api_key="AIzaSyBrIzyi5AGaQZ5CXVBQPVjZmiM7hCjoZpc")
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------------
# Helper: Parse Firebase Errors
# -------------------------------
def parse_firebase_error(e):
    try:
        error_json = e.args[1]  # Pyrebase stores error in second arg
        error = json.loads(error_json)['error']['message']

        if error == "EMAIL_EXISTS":
            return "This email is already in use. Try logging in instead."
        elif error == "EMAIL_NOT_FOUND":
            return "No account found with this email."
        elif error == "INVALID_PASSWORD":
            return "Incorrect password. Please try again."
        elif error == "WEAK_PASSWORD : Password should be at least 6 characters":
            return "Password too weak. Use at least 6 characters."
        else:
            return error.replace("_", " ").capitalize()
    except:
        return str(e)

# -------------------------------
# Session State
# -------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="✨ R-Gen AI", page_icon="⚡", layout="wide")
st.title("✨ R-Gen AI 🚀")
st.write("Your AI sidekick for hustles.")

# -------------------------------
# Auth Section
# -------------------------------
if not st.session_state.user:
    choice = st.radio("Login or Sign Up", ["Login", "Sign Up"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Sign Up":
        if st.button("Create Account"):
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success("✅ Account created! Please log in.")
            except Exception as e:
                st.error(f"❌ {parse_firebase_error(e)}")

    elif choice == "Login":
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.success("✅ Logged in successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"❌ {parse_firebase_error(e)}")

# -------------------------------
# Chatbot Section
# -------------------------------
else:
    st.subheader(f"Welcome, {st.session_state.user['email']} 👋")

    # Show past messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        # Loading animation
        placeholder = st.empty()
        for i in range(6):
            placeholder.markdown("⏳ Thinking" + "." * (i % 4))
            time.sleep(0.3)

        # AI response
        conversation_text = f"You are R-Gen AI, a helpful assistant.\nUser: {prompt}"
        response = model.generate_content(conversation_text)
        bot_message = response.text

        placeholder.markdown(bot_message)
        st.session_state.messages.append({"role": "assistant", "content": bot_message})

    if st.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()


