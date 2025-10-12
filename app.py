import streamlit as st
import time
import google.generativeai as genai
import datetime

# -------------------------------
# Configure Gemini AI (replace with your key)
# -------------------------------
genai.configure(api_key="AIzaSyDO1ZV6ep36DlC6FYk_uMrigYuWzjNG9hM")
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------------
# In-memory user DB (demo)
# -------------------------------
users_db = {"test@example.com": "1234"}

# -------------------------------
# Session state & trial
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_visit" not in st.session_state:
    st.session_state.first_visit = datetime.datetime.now()

# -------------------------------
# Page config + header
# -------------------------------
st.set_page_config(page_title="✨ R-Gen AI", page_icon="⚡", layout="wide")

# header row: title left, spacer, (we'll render auth box absolutely)
col1, col2 = st.columns([8, 1])
with col1:
    st.markdown("<h1 style='margin:0'>✨ R-Gen AI 🚀</h1>", unsafe_allow_html=True)
    st.write("Your AI sidekick for hustles 🚀")

# -------------------------------
# CSS for top-right segmented control
# -------------------------------
st.markdown(
    """
    <style>
    /* the container that will hold the two buttons */
    .auth-top-right {
        position: fixed;
        top: 18px;
        right: 24px;
        z-index: 9999;
        background: transparent;
        padding: 0;
    }

    /* style Streamlit button wrappers inside the container */
    .auth-top-right .stButton > button {
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
        border: 1px solid #cfcfcf;
        margin: 0;
        min-width: 110px;
        height: 38px;
        box-shadow: none;
    }

    /* left button (signup) - outline */
    .auth-top-right .stButton:first-child > button {
        background: #ffffff;
        color: #333333;
        border-right: none;
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;
    }

    /* right button (login) - active blue */
    .auth-top-right .stButton:last-child > button {
        background: #1f6feb;
        color: #fff;
        border-left: none;
        border-top-left-radius: 0;
        border-bottom-left-radius: 0;
    }

    /* subtle hover */
    .auth-top-right .stButton > button:hover {
        opacity: 0.92;
    }

    /* small box around both to match screenshot feel */
    .auth-top-right-wrapper {
        border-radius: 10px;
        padding: 4px;
        background: rgba(255,255,255,0.9);
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Render the two buttons in a custom floating area
# We create a minimal wrapper and then render two Streamlit buttons inside columns.
st.markdown('<div class="auth-top-right"><div class="auth-top-right-wrapper">', unsafe_allow_html=True)

# Create two tiny columns so the buttons are adjacent
c1, c2 = st.columns([1, 1], gap="small")
with c1:
    signup_clicked = st.button("Signup", key="seg_signup")
with c2:
    login_clicked = st.button("Login", key="seg_login")

st.markdown('</div></div>', unsafe_allow_html=True)

# -------------------------------
# Signup/Login modal-like behavior (simple)
# -------------------------------
# We'll show a small form below the header only if a button was clicked.
if signup_clicked:
    st.info("Create an account")
    email = st.text_input("Email for signup", key="signup_email")
    password = st.text_input("Password (min 6 chars)", type="password", key="signup_pass")
    if st.button("Create Account", key="create_acc"):
        if not email or "@" not in email:
            st.error("Please enter a valid email address.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")
        elif email in users_db:
            st.error("Email already registered. Try logging in.")
        else:
            users_db[email] = password
            st.success("Account created — you can now log in.")

if login_clicked:
    st.info("Log in to R-Gen AI")
    lemail = st.text_input("Email for login", key="login_email")
    lpass = st.text_input("Password", type="password", key="login_pass")
    if st.button("Log In", key="do_login"):
        if lemail in users_db and users_db[lemail] == lpass:
            st.session_state.logged_in = True
            st.success("Logged in! 🎉")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")

# -------------------------------
# Trial and chat area
# -------------------------------
days_passed = (datetime.datetime.now() - st.session_state.first_visit).days
trial_limit = 4
trial_over = (days_passed >= trial_limit) and not st.session_state.logged_in

# show countdown (visible)
if not st.session_state.logged_in:
    days_left = max(0, trial_limit - days_passed)
    st.markdown(f"**Free trial:** {days_left} day(s) left. After that, please Sign Up or Login to continue.")

if trial_over:
    st.warning("⚠️ Your 4-day free trial expired. Please Sign Up or Login to continue.")
else:
    # display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # chat input and response
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        # animated 3-dot wave (nice)
        placeholder = st.empty()
        wave_frames = ["<span style='font-size:26px'>● ○ ○</span>",
                       "<span style='font-size:26px'>○ ● ○</span>",
                       "<span style='font-size:26px'>○ ○ ●</span>"]
        for _ in range(8):
            for frame in wave_frames:
                placeholder.markdown(frame, unsafe_allow_html=True)
                time.sleep(0.18)

        # generate response
        conversation_text = (
            "You are R-Gen AI, a helpful assistant. "
            "Correct spelling/grammar if needed and answer clearly. "
            "Do NOT repeat the user’s question.\n\n"
            f"User: {prompt}"
        )
        try:
            response = model.generate_content(conversation_text)
            bot_message = response.text
        except Exception as e:
            bot_message = "Sorry — an error happened while contacting the AI."

        placeholder.markdown(bot_message)
        st.session_state.messages.append({"role": "assistant", "content": bot_message})

# Optional small logout button if logged in
if st.session_state.logged_in:
    if st.button("Logout", key="logout_small"):
        st.session_state.logged_in = False
        st.experimental_rerun()










