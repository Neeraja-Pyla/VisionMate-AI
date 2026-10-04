# 👁️ VisionMate AI — AI Vision Chatbot

VisionMate AI is a multimodal AI chatbot that allows users to upload an image and interact with it using natural-language questions.

The application uses Google's Gemini AI to understand visual content, describe images, identify objects, read visible text, and answer follow-up questions through an interactive chat interface.

## 🚀 Live Demo

🔗 **Live Application:**  
[https://YOUR-STREAMLIT-APP-URL](https://visionmate-ai-gjlneafcfqshnhe3bsz9na.streamlit.app/)

## 📌 Features

- 🖼️ Upload images and analyze them using AI
- 💬 Ask natural-language questions about uploaded images
- 🔍 Identify objects and visual elements
- 📝 Extract and explain visible text
- 📖 Generate detailed image descriptions
- 🧠 Understand what is happening in an image
- 💬 Conversational follow-up questions
- 📚 Maintain chat history during the session
- 🎨 Clean and responsive Streamlit interface
- 🔐 API key protected using environment variables / Streamlit Secrets

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web interface |
| Google Gemini API | Multimodal AI / image understanding |
| Google GenAI SDK | Gemini API integration |
| Pillow | Image processing |
| python-dotenv | Environment variable management |

## 🏗️ Project Structure

```text
VisionMate-AI/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
└── .env                 # Local only — DO NOT upload
