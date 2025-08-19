import streamlit as st
import time
import google.generativeai as genai
import stripe

# Configure your API keys
genai.configure(api_key=st.secrets["AIzaSyB1kHYm_pPeam1v9hAyhJcexIgZraEj5Ek"])
stripe.api_key = st.secrets["pk_test_51RxbHpRIrSebCqVdcPOEd8ric0lez0EPZSU1kk3QKjCddHuEEyCqoSXLU5MbPkP2qbTp3CkzZkgjUBipyN3xNFGC00rSYjwt63"]

model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit page setup
st.set_page_config(page_title="✨ R-Gen AI", page_icon="⚡", layout="wide")

# Header bar with PNG icon
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1 style="margin: 0;">✨ R-Gen AI</h1>
        <img src="https://img.icons8.com/fluency/48/rocket.png" width="40">
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Your AI sidekick 🚀")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize payment state
if "paid" not in st.session_state:
    st.session_state.paid = False

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Premium paywall
if not st.session_state.paid:
    st.warning("Upgrade to **R-Gen AI Premium** to unlock extended responses and bonus features!")
    if st.button("Pay $5 for Premium"):
        # In real app, here you would create a Stripe checkout session
        st.session_state.paid = True
        st.success("Payment received! You now have access to premium features.")

# Chat input
if prompt := st.chat_input("Type your message..."):

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Typing animation (wavy dots)
    placeholder = st.empty()
    wave = ["·    ", " ·   ", "  ·  ", "   · ", "  ·  ", " ·   "]
    for i in range(12):
        placeholder.markdown(f"**{wave[i % len(wave)]}**")
        time.sleep(0.2)

    # Build AI prompt
    conversation_text = (
        "You are R-Gen AI, a helpful assistant. "
        "Correct spelling/grammar and answer clearly. "
        "Do NOT repeat the user’s question.\n\n"
        f"User: {prompt}"
    )

    # If user is paid, add bonus instructions
    if st.session_state.paid:
        conversation_text += "\nAssistant: Give a more detailed, premium-level response."

    # Generate AI response
    response = model.generate_content(conversation_text)
    bot_message = response.text

    # Affiliate link integration (example)
    if "ai course" in prompt.lower():
        bot_message += "\n\n💡 Check out this AI course [here](https://www.udemy.com/course/artificial-intelligence/?ref=YOUR_AFFILIATE_CODE)!"

    # Show AI response
    placeholder.markdown(bot_message)
    st.session_state.messages.append({"role": "assistant", "content": bot_message})



