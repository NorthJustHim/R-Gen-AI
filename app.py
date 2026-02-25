import streamlit as st
import time
import google.generativeai as genai
import datetime
import json
import os

# -------------------------------
# Configure Gemini AI
# -------------------------------
genai.configure(api_key="AIzaSyDO1ZV6ep36DlC6FYk_uMrigYuWzjNG9hM")
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------------
# JSON "database" setup
# -------------------------------
DB_FILE = "users.json"

# Load users from file
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        users_db = json.load(f)
else:
    users_db = {"test@example.com": "1234"}

# Helper to save users
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

# -------------------------------
# Page config + header
# -------------------------------
st.set_page_config(page_title="✨ R-Gen AI", page_icon="⚡", layout="wide")
col1, col2 = st.columns([8, 1])
with col1:
    st.markdown("<h1 style='margin:0'>✨ R-Gen AI 🚀</h1>", unsafe_allow_html=True)
    st.write("Your AI sidekick for hustles 🚀")

# -------------------------------
# CSS for top-right buttons
# -------------------------------
st.markdown("""
<style>
.auth-top-right {position: fixed; top: 18px; right: 24px; z-index: 9999; background: transparent; padding: 0;}
.auth-top-right .stButton > button {border-radius: 8px; padding: 8px 18px; font-weight: 600; border: 1px solid #cfcfcf; margin: 0; min-width: 110px; height: 38px; box-shadow: none;}
.auth-top-right .stButton:first-child > button {background: #ffffff; color: #333333; border-right: none; border-top-right-radius: 0; border-bottom-right-radius: 0;}
.auth-top-right .stButton:last-child > button {background: #1f6feb; color: #fff; border-left: none; border-top-left-radius: 0; border-bottom-left-radius: 0;}
.auth-top-right .stButton > button:hover {opacity: 0.92;}
.auth-top-right-wrapper {border-radius: 10px; padding: 4px; background: rgba(255,255,255,0.9); box-shadow: 0 6px 18px rgba(0,0,0,0.06); display: inline-block;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Floating Signup/Login buttons
# -------------------------------
st.markdown('<div class="auth-top-right"><div class="auth-top-right-wrapper">', unsafe_allow_html=True)
c1, c2 = st.columns([1,1], gap="small")
with c1:
    if st.button("Signup", key="seg_signup"):
        st.session_state.show_signup = True
        st.session_state.show_login = False
with c2:
    if st.button("Login", key="seg_login"):
        st.session_state.show_signup = False
        st.session_state.show_login = True
st.markdown('</div></div>', unsafe_allow_html=True)

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
# Trial and chat area
# -------------------------------
days_passed = (datetime.datetime.now() - st.session_state.first_visit).days
trial_limit = 4
trial_over = (days_passed >= trial_limit) and not st.session_state.logged_in

if not st.session_state.logged_in:
    days_left = max(0, trial_limit - days_passed)
    st.markdown(f"**Free trial:** {days_left} day(s) left. After that, please Sign Up or Login to continue.")

if trial_over:
    st.warning("⚠️ Your 4-day free trial expired. Please Sign Up or Login to continue.")
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role":"user","content":prompt})
        st.chat_message("user").markdown(prompt)
        placeholder = st.empty()
        wave_frames = ["<span style='font-size:26px'>● ○ ○</span>","<span style='font-size:26px'>○ ● ○</span>","<span style='font-size:26px'>○ ○ ●</span>"]
        for _ in range(8):
            for frame in wave_frames:
                placeholder.markdown(frame, unsafe_allow_html=True)
                time.sleep(0.18)
        conversation_text = (
            "You are R-Gen AI, a helpful assistant. "
            "Correct spelling/grammar if needed and answer clearly. "
            "Do NOT repeat the user’s question.\n\n"
            f"User: {prompt}"
        )
        try:
            response = model.generate_content(conversation_text)
            bot_message = response.text
        except Exception:
            bot_message = "Sorry — an error happened while contacting the AI."
        placeholder.markdown(bot_message)
        st.session_state.messages.append({"role":"assistant","content":bot_message})

# -------------------------------
# Logout
# -------------------------------
if st.session_state.logged_in:
    if st.button("Logout", key="logout_small"):
        st.session_state.logged_in = False
        st.experimental_rerun()
