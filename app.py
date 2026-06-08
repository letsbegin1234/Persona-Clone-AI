import os
from chat_parser import parse_chat
from embeddings import embed_text
from vector_store import VectorStore
from retriever import retrieve_examples
from generator import generate_reply
from style_analyzer import style_summary
from config import *

print("Welcome to Persona Clone AI!")

chat_file = input("Enter chat file path (default: data/chat.txt): ").strip()
if not chat_file:
    chat_file = "data/chat.txt"

if not os.path.exists(chat_file):
    print(f"File {chat_file} not found!")
    exit()

target_person = input("Enter the exact name of the person to replicate (e.g., Suraj ESE): ").strip()
if not target_person:
    print("Name is required!")
    exit()

persona_name = target_person  # Use same name for target and persona

print(f"\nLoading chat for {persona_name}...")

messages, pairs, full_chat = parse_chat(chat_file, target_person)

if not messages:
    print(f"No messages found for '{target_person}'! Please check the spelling.")
    exit()

print(f"{len(messages)} messages loaded")
print(f"{len(pairs)} Q→A pairs extracted")

# Embed only the QUESTION (incoming message) for better query matching
questions = [u for u, a in pairs]
embeddings = embed_text(questions)

vector_db = VectorStore(len(embeddings[0]))
vector_db.add(embeddings, pairs)

# Build comprehensive style profile
style = style_summary(messages)

print(f"\nStyle profile built:")
print(style.get("style_text", ""))
print(f"\nSample messages: {len(style.get('sample_messages', []))}")
print(f"\nPersona ready — chatting as {persona_name}\n")

# Conversation history for multi-turn context
conversation_history = []

while True:
    try:
        user_input = input("You: ").strip()
    except KeyboardInterrupt:
        break

    if user_input.lower() == "exit":
        break

    if not user_input:
        continue

    # Build context window for retrieval matching the format in chat_parser
    query_parts = []
    # Take up to 2 recent messages from history
    for turn in conversation_history[-2:]:
        query_parts.append(turn["content"])
    query_parts.append(user_input)
    
    query_context = " | ".join(query_parts)

    # Retrieve similar conversation examples using the multi-message context
    examples = retrieve_examples(vector_db, embed_text, query_context)

    # Debug: show what was retrieved
    print(f"\n[DEBUG] Retrieved {len(examples)} examples:")
    for u, a, score in examples[:3]:
        print(f"  [{score:.3f}] Q: {u[:50]}... → A: {a[:50]}")

    # Add user message to history
    conversation_history.append({"role": "user", "content": user_input})

    # Generate reply with full context
    reply = generate_reply(user_input, examples, style, persona_name, conversation_history)

    # Add assistant reply to history
    conversation_history.append({"role": "assistant", "content": reply})

    # Keep history bounded
    if len(conversation_history) > CONVERSATION_HISTORY_LENGTH * 2:
        conversation_history = conversation_history[-(CONVERSATION_HISTORY_LENGTH * 2):]

    print(f"\n{persona_name}: {reply}\n")