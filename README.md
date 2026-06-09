# Persona Clone AI

Persona Clone AI is an interactive terminal-based chat application that replicates the texting style, vocabulary, and tone of any of your WhatsApp contacts using RAG (Retrieval-Augmented Generation) and the Google Gemini API.

It analyzes your exported WhatsApp chats or a user-provided questionnaire, builds a comprehensive linguistic profile, and uses cosine-similarity search to pull contextually relevant past messages to accurately mimic your friend's conversational behavior.

## Features

- **Dual Modes of Operation**:
  - **Chat Upload Mode**: Automatically extract participants and styles from your WhatsApp export file.
  - **Questionnaire Mode**: Create a persona from scratch by answering an interactive questionnaire about their texting habits, without needing a chat file.
- **Multilingual Code-Switching**: Automatically detects if the person chats in native languages mixed with English (supports Hindi, Telugu, Tamil, Kannada, Bengali, Marathi, Malayalam, Gujarati, and Punjabi transliteration).
- **Nickname & Address Term Detection**: Detects common nicknames (e.g., bro, bhai, macha, anna) and their frequency, ensuring the AI addresses you naturally.
- **Rich Style Profiling**: Analyzes message length, emoji habits, capitalization, punctuation, and frequent vocabulary to build a deeply accurate profile.
- **RAG-Powered Memory**: Uses `SentenceTransformers` and `FAISS` to find real past conversations matching your current context (in Chat Upload Mode).
- **Multi-Turn Context**: Remembers the flow of the current conversation, so the AI responds appropriately to the situation.

## Prerequisites

- Python 3.9+
- A Google Gemini API Key

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd persona_clone_ai_project_chatgpt
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Gemini API Key:**
   Create a `.env` file in the root directory and add your API key:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```

## Usage

Run the main application:

```bash
python3 app.py
```

The script will ask you to choose a mode:

1. **Upload a WhatsApp chat file**: Provide the path to your WhatsApp export file and the name of the person you want to replicate.
2. **Answer a questionnaire**: Interactively build a persona by answering questions about their texting style, typical message length, language, nicknames, and providing a few sample messages.

Start chatting! Type `exit` at any time to leave.

### Getting WhatsApp Chat Data (for Mode 1)

1. Open a WhatsApp chat on your phone.
2. Tap the three dots (menu) -> **More** -> **Export Chat**.
3. Select **Without Media**.
4. Save the `.txt` file and place it in the `data/` directory of this project (e.g., `data/chat.txt`).

*(Note: The `data/` directory is added to `.gitignore` by default to protect your privacy. Do not commit your personal chats to GitHub!)*

## Technical Stack

- **LLM**: Google Gemini 2.5/3.1 Flash via `google-genai`
- **Embeddings**: `paraphrase-multilingual-MiniLM-L12-v2` via `sentence-transformers`
- **Vector DB**: `faiss-cpu` (Inner Product / Cosine Similarity)
- **Environment**: `python-dotenv`
