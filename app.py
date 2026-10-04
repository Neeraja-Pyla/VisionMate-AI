
import streamlit as st
from google import genai
from PIL import Image
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="VisionMate AI",
    page_icon="👁️",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #172554);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.stButton button {
    background: #6366f1;
    color: white;
    border-radius: 10px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("👁️ VisionMate AI")
st.caption(
    "Your intelligent visual assistant — Upload. Ask. Understand."
)

st.divider()

# Initialize Gemini
if not API_KEY:
    st.error("API key missing. Please configure your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# Session history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None

# Sidebar
with st.sidebar:
    st.header("⚙️ Vision Controls")

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Your uploaded image",
                 use_container_width=True)

        st.session_state.image_bytes = image

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("Powered by Google Gemini Vision")

# Main interface
st.subheader("💬 Chat with your image")

if st.session_state.image_bytes is None:
    st.info("Upload an image from the sidebar to begin.")

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input(
    "Ask anything about your image..."
)

if prompt:
    if st.session_state.image_bytes is None:
        st.warning("Please upload an image first.")
    else:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing your image..."):
                try:
                    history_text = ""

                    for msg in st.session_state.messages[:-1]:
                        history_text += (
                            f'{msg["role"]}: {msg["content"]}\n'
                        )

                    instruction = f"""
                    You are VisionMate AI, a helpful visual assistant.

                    Analyze the provided image carefully.

                    Answer the user's question in simple,
                    clear language.

                    Never invent details that cannot be seen.
                    If uncertain, clearly state uncertainty.

                    Previous conversation:
                    {history_text}

                    Current question:
                    {prompt}
                    """

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=[
                            instruction,
                            st.session_state.image_bytes
                        ]
                    )

                    answer = response.text or (
                        "I could not generate a response."
                    )

                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:
                    st.error(f"An error occurred: {e}")

st.divider()

st.caption(
    "VisionMate AI | Multimodal Generative AI Project"
)