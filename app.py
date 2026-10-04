import os
import time

import streamlit as st
from google import genai
from PIL import Image
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VisionMate AI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #111827 50%,
            #172554 100%
        );
    }

    /* Main title */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 1.1rem;
        opacity: 0.8;
        margin-bottom: 25px;
    }

    /* Cards */
    .feature-card {
        padding: 18px;
        border-radius: 15px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        min-height: 130px;
    }

    .feature-title {
        font-size: 1.05rem;
        font-weight: 700;
    }

    .feature-text {
        font-size: 0.9rem;
        opacity: 0.75;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.15);
        font-weight: 600;
    }

    /* Chat input */
    .stChatInput {
        border-radius: 12px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0b1120;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHECK API KEY
# ============================================================

if not API_KEY:

    st.error(
        "❌ Gemini API key is missing."
    )

    st.info(
        """
        For local development:

        Create a `.env` file containing:

        GEMINI_API_KEY=YOUR_API_KEY

        For Streamlit Cloud:

        Go to:
        App → Settings → Secrets

        and add:

        GEMINI_API_KEY = "YOUR_API_KEY"
        """
    )

    st.stop()


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=API_KEY)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "image" not in st.session_state:
    st.session_state.image = None


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">👁️ VisionMate AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'See the world through AI — upload an image, ask questions, '
    'and get intelligent visual insights.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Vision Controls")

    uploaded_file = st.file_uploader(
        "📤 Upload an image",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp"
        ]
    )

    if uploaded_file:

        try:

            image = Image.open(
                uploaded_file
            ).convert("RGB")

            st.session_state.image = image

            st.image(
                image,
                caption="Uploaded Image",
                use_container_width=True
            )

            st.success(
                "✅ Image ready for analysis"
            )

        except Exception as e:

            st.error(
                f"Unable to read image: {e}"
            )

    st.divider()

    st.subheader("✨ Capabilities")

    st.markdown(
        """
        👁️ **Image Understanding**

        💬 **Visual Question Answering**

        📝 **Text Recognition**

        🧠 **Scene Analysis**

        🔎 **Object Identification**

        🔄 **Follow-up Questions**
        """
    )

    st.divider()

    st.caption(
        "Powered by Google Gemini"
    )

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# MAIN AREA
# ============================================================

st.subheader("💬 Chat with your image")


# ============================================================
# NO IMAGE MESSAGE
# ============================================================

if st.session_state.image is None:

    st.info(
        "👈 Upload an image from the sidebar to start."
    )


# ============================================================
# FEATURE CARDS
# ============================================================

if st.session_state.image is not None:

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">

            <div class="feature-title">
            🔍 Describe
            </div>

            <div class="feature-text">
            Understand what's happening in the image.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">

            <div class="feature-title">
            📝 Read Text
            </div>

            <div class="feature-text">
            Identify and explain visible text.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="feature-card">

            <div class="feature-title">
            🧠 Analyze
            </div>

            <div class="feature-text">
            Ask questions and explore the image.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

if st.session_state.image is not None:

    st.markdown("### 💡 Suggested questions")

    st.caption(
        "Copy one of these questions into the chat box:"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.code(
            "Describe this image in detail.",
            language=None
        )

        st.code(
            "What objects are visible in this image?",
            language=None
        )

    with col2:

        st.code(
            "What text is visible in this image?",
            language=None
        )

        st.code(
            "Explain what is happening in this image.",
            language=None
        )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Ask anything about your image..."
)


# ============================================================
# PROCESS USER QUESTION
# ============================================================

if prompt:

    # ---------------------------------------------
    # Check image
    # ---------------------------------------------

    if st.session_state.image is None:

        st.warning(
            "⚠️ Please upload an image first."
        )

        st.stop()


    # ---------------------------------------------
    # Display user message
    # ---------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)


    # ---------------------------------------------
    # Generate AI response
    # ---------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "👁️ VisionMate is analyzing the image..."
        ):

            try:

                # ---------------------------------
                # Build conversation context
                # ---------------------------------

                conversation_history = ""

                for message in st.session_state.messages:

                    conversation_history += (
                        f'{message["role"]}: '
                        f'{message["content"]}\n'
                    )


                # ---------------------------------
                # AI instruction
                # ---------------------------------

                instruction = f"""
You are VisionMate AI, an intelligent multimodal
visual assistant.

Your job is to analyze the provided image and answer
the user's questions accurately.

IMPORTANT RULES:

1. Only describe information that can reasonably
   be determined from the image.

2. Do not invent objects, people, text, events,
   or details.

3. If something is unclear, say that it is unclear.

4. Answer in simple, useful language.

5. When appropriate, use bullet points.

6. For visible text, reproduce only text that
   can reasonably be read.

7. For image analysis questions, explain your
   reasoning briefly but do not reveal hidden
   chain-of-thought.

Previous conversation:

{conversation_history}

Current user question:

{prompt}
"""


                # ---------------------------------
                # Retry mechanism
                # ---------------------------------

                response = None

                max_attempts = 3

                for attempt in range(
                    max_attempts
                ):

                    try:

                        response = client.models.generate_content(

                            model="gemini-3.5-flash-lite",

                            contents=[
                                instruction,
                                st.session_state.image
                            ]
                        )

                        break


                    except Exception as api_error:

                        error_text = str(
                            api_error
                        )


                        # -------------------------
                        # Temporary server overload
                        # -------------------------

                        if (
                            "503" in error_text
                            or
                            "UNAVAILABLE" in error_text
                        ):

                            if attempt < max_attempts - 1:

                                wait_time = (
                                    2 ** attempt
                                )

                                time.sleep(
                                    wait_time
                                )

                            else:

                                raise


                        else:

                            raise


                # ---------------------------------
                # Validate response
                # ---------------------------------

                if response is None:

                    st.error(
                        "The AI model did not return a response."
                    )

                    st.stop()


                answer = (
                    response.text
                    if response.text
                    else
                    "I couldn't generate a response."
                )


                # ---------------------------------
                # Display answer
                # ---------------------------------

                st.markdown(answer)


                # ---------------------------------
                # Save assistant message
                # ---------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


            # =================================================
            # ERROR HANDLING
            # =================================================

            except Exception as e:

                error_text = str(e)


                if (
                    "503" in error_text
                    or
                    "UNAVAILABLE" in error_text
                ):

                    st.error(
                        "⚠️ Gemini is temporarily experiencing "
                        "high demand."
                    )

                    st.info(
                        "Please wait a few seconds and try "
                        "your question again."
                    )


                elif (
                    "404" in error_text
                    or
                    "NOT_FOUND" in error_text
                ):

                    st.error(
                        "❌ The configured Gemini model "
                        "is unavailable for this API key."
                    )

                    st.info(
                        "Check the currently available models "
                        "for your Gemini API account."
                    )


                elif (
                    "401" in error_text
                    or
                    "403" in error_text
                ):

                    st.error(
                        "🔐 Gemini API authentication failed."
                    )

                    st.info(
                        "Check your GEMINI_API_KEY in "
                        "Streamlit Cloud Secrets."
                    )


                elif (
                    "429" in error_text
                    or
                    "RESOURCE_EXHAUSTED" in error_text
                ):

                    st.error(
                        "⏳ Gemini API usage limit reached."
                    )

                    st.info(
                        "Please wait and try again later."
                    )


                else:

                    st.error(
                        "❌ Something went wrong while "
                        "processing your request."
                    )

                    st.caption(
                        f"Technical details: {error_text}"
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "VisionMate AI • Multimodal Generative AI • "
    "Python + Streamlit + Gemini"
)