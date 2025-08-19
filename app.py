import streamlit as st
import time
import google.generativeai as genai
import stripe

# -------------------------------
# Configure Stripe
# -------------------------------
stripe.api_key = "sk_test_51RxbHpRIrSebCqVdttX2rHUr75ZF0pyTBDGe02RyYZrkoyIXjJnnPVeY3vGgvaBNGVLWhEegLlXmQOoFrf7raiM2007bsr4MLy"  # Replace with your Stripe secret key

# Initialize access flag
if "paid" not in st.session_state:
    st.session_state.paid = False

# -------------------------------
# Configure Gemini AI
# -------------------------------
genai.configure(api_key="AIzaSyB1kHYm_pPeam1v9hAyhJcexIgZraEj5Ek")  # Replace with your Gemini API key
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------------
# Streamlit page config
# -------------------------------
st.set_page_config(page_title="✨ R-Gen AI", page_icon="⚡", layout="wide")

# Header with PNG icon
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
# Payment Section
# -------------------------------
if not st.session_state.paid:
    st.write("Click below to pay $5 to unlock the chatbot:")

    if st.button("Pay $5"):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'R-Gen AI Access'},
                        'unit_amount': 500,  # $5 in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://revalutiongeneration-ai.streamlit.app/',  # Replace with your Streamlit app URL
                cancel_url='https://revalutiongeneration-ai.streamlit.app/',
            )
            st.markdown(f"[Click here to pay]({session.url})", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error creating checkout session: {e}")

# -------------------------------
# Chatbot Section
# -------------------------------
else:
    st.write("✅ Access granted! You can now chat with R-Gen AI.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

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





