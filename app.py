import streamlit as st
import time
import google.generativeai as genai
import datetime
import json
import os

# -------------------------------
# Configure Gemini AI
# -------------------------------
genai.configure(api_key="AIzaSyChy_4shVmQO6VfWgEykID34Kn03gKI0CI")
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------------
# JSON "database" setup
# -------------------------------
DB_FILE = "users.json"

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        users_db = json.load(f)
else:
    users_db = {"test@example.com": "1234"}

def save_users():
    with open(DB_FILE, "w") as f:
        json.dump(users_db, f)

# -------------------------------
# Session state
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_visit" not in st.session_state:
    st.session_state.first_visit = datetime.datetime.now()
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = [{"name": "Default Chat", "messages": []}]
if "active_chat" not in st.session_state:
    st.session_state.active_chat = 0  # index of current chat

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(page_title="✨ R-Gen AI", page_icon="⚡", layout="wide")

# -------------------------------
# Sidebar: Your Chats
# -------------------------------
with st.sidebar:
    st.markdown("<h2>Your Chats</h2>", unsafe_allow_html=True)
    for i, chat in enumerate(st.session_state.chat_sessions):
        if st.button(chat["name"], key=f"chat_{i}"):
            st.session_state.active_chat = i
    st.markdown("---")
    if st.button("➕ New Chat", key="new_chat"):
        st.session_state.chat_sessions.append({"name": f"Chat {len(st.session_state.chat_sessions)+1}", "messages": []})
        st.session_state.active_chat = len(st.session_state.chat_sessions) - 1

# -------------------------------
# Floating Signup/Login buttons
# -------------------------------
st.markdown('<div style="position: fixed; top: 18px; right: 24px; z-index: 9999;">', unsafe_allow_html=True)
c1, c2 = st.columns([1,1], gap="small")
with c1:
    if st.button("Signup", key="seg_signup"):
        st.session_state.show_signup = True
        st.session_state.show_login = False
with c2:
    if st.button("Login", key="seg_login"):
        st.session_state.show_signup = False
        st.session_state.show_login = True
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Signup form
# -------------------------------
if st.session_state.show_signup:
    st.info("Create an account")
    signup_email = st.text_input("Email for signup", key="signup_email")
    signup_pass = st.text_input("Password (min 6 chars)", type="password", key="signup_pass")
    if st.button("Create Account", key="create_acc"):
        if not signup_email or "@" not in signup_email:
            st.error("Please enter a valid email address.")
        elif len(signup_pass) < 6:
            st.error("Password must be at least 6 characters.")
        elif signup_email in users_db:
            st.error("Email already registered. Try logging in.")
        else:
            users_db[signup_email] = signup_pass
            save_users()
            st.success("Account created — you can now log in.")

# -------------------------------
# Login form
# -------------------------------
if st.session_state.show_login:
    st.info("Log in to R-Gen AI")
    login_email = st.text_input("Email for login", key="login_email")
    login_pass = st.text_input("Password", type="password", key="login_pass")
    if st.button("Log In", key="do_login"):
        if login_email in users_db and users_db[login_email] == login_pass:
            st.session_state.logged_in = True
            st.session_state.show_login = False
            st.session_state.show_signup = False
            st.success(f"Logged in! 🎉 Welcome, {login_email}")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")

# -------------------------------
# Active chat display
# -------------------------------
active_chat = st.session_state.chat_sessions[st.session_state.active_chat]
st.markdown(f"### {active_chat['name']}")

# show messages
for msg in active_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# chat input
if prompt := st.chat_input("Type your message..."):
    active_chat["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # animated 3-dot wave
    placeholder = st.empty()
    wave_frames = ["<span style='font-size:26px'>● ○ ○</span>",
                   "<span style='font-size:26px'>○ ● ○</span>",
                   "<span style='font-size:26px'>○ ○ ●</span>"]
    for _ in range(8):
        for frame in wave_frames:
            placeholder.markdown(frame, unsafe_allow_html=True)
            time.sleep(0.18)

    # AI response with error handling
    conversation_text = (
        "You are R-Gen AI, a helpful assistant. "
        "Correct spelling/grammar if needed and answer clearly. "
        "Do NOT repeat the user’s question.\n\n"
        f"User: {prompt}"
    )
    try:
        response = model.generate_content(conversation_text)
        # safer access to AI response
        if hasattr(response, "text"):
            bot_message = response.text
        elif hasattr(response, "candidates") and len(response.candidates) > 0:
            bot_message = response.candidates[0].content
        else:
            bot_message = "AI did not return a response."
    except Exception as e:
        bot_message = f"Sorry — an error happened while contacting the AI.\nDetails: {e}"

    placeholder.markdown(bot_message)
    active_chat["messages"].append({"role": "assistant", "content": bot_message})

# -------------------------------
# Logout
# -------------------------------
if st.session_state.logged_in:
    if st.button("Logout", key="logout_small"):
        st.session_state.logged_in = False
        st.experimental_rerun()
