# Persona Clone AI

Persona Clone AI is an interactive terminal-based chat application that replicates the texting style, vocabulary, and tone of any of your WhatsApp contacts using RAG (Retrieval-Augmented Generation) and the Google Gemini API.

It analyzes your exported WhatsApp chats, builds a comprehensive linguistic profile, and uses cosine-similarity search to pull contextually relevant past messages to accurately mimic your friend's conversational behavior.

## Features

- **Dynamic Persona Selection**: Automatically extracts participants from your WhatsApp export file.
- **RAG-Powered Memory**: Uses `SentenceTransformers` and `FAISS` to find real past conversations matching your current context.
- **Rich Style Profiling**: Analyzes message length, Telugu-English code-switching, emoji habits, capitalization, and frequent vocabulary.
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

## Getting WhatsApp Chat Data

1. Open a WhatsApp chat on your phone.
2. Tap the three dots (menu) -> **More** -> **Export Chat**.
3. Select **Without Media**.
4. Save the `.txt` file and place it in the `data/` directory of this project (e.g., `data/chat.txt`).

*(Note: The `data/` directory is added to `.gitignore` by default to protect your privacy. Do not commit your personal chats to GitHub!)*

## Usage

Run the main application:

```bash
python3 app.py
```

The script will ask you for:
1. The path to your WhatsApp export file.
2. Which person from the chat you want to replicate.
3. What name to give the AI persona.

Start chatting! Type `exit` at any time to leave.

## Technical Stack

- **LLM**: Google Gemini 2.5/3.1 Flash via `google-genai`
- **Embeddings**: `paraphrase-multilingual-MiniLM-L12-v2` via `sentence-transformers`
- **Vector DB**: `faiss-cpu` (Inner Product / Cosine Similarity)
- **Environment**: `python-dotenv`
