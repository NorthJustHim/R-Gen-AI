import streamlit as st
import time
import google.generativeai as genai

# -------------------------------
# Configure Gemini AI
# -------------------------------
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # replace with your key
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

# -------------------------------
# Streamlit page config
# -------------------------------
st.set_page_config(page_title="✨ R-Gen AI", page_icon="⚡", layout="wide")

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
# Auth Section
# -------------------------------
if not st.session_state.logged_in:
    st.subheader("Sign Up or Log In")

    option = st.radio("Choose:", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

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

# -------------------------------
# Chatbot Section
# -------------------------------
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

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()




