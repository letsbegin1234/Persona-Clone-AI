from google import genai
from config import GEMINI_API_KEY, MAX_OUTPUT_TOKENS

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def generate_reply(user_input, examples, style, persona_name, conversation_history=None):
    """
    Generate a persona-accurate WhatsApp reply using Gemini.

    Args:
        user_input (str): The user's latest message.
        examples (list): Retrieved examples [(user_msg, reply, score), ...]
        style (dict): Style profile from style_analyzer.
        conversation_history (list): Recent conversation turns
                                     [{"role": "user"/"assistant", "content": "..."}]

    Returns:
        str: Generated reply in the persona's style.
    """

    # --- Build the sample messages block ---
    sample_msgs = style.get("sample_messages", [])
    sample_block = ""
    if sample_msgs:
        sample_block = "\n".join(f'  "{m}"' for m in sample_msgs[:8])

    # --- Build the retrieved examples block ---
    examples_block = ""
    if examples:
        for user_msg, reply, score in examples[:5]:
            examples_block += f"  Other person: {user_msg}\n  {persona_name}: {reply}\n\n"

    # --- Build conversation history block ---
    history_block = ""
    if conversation_history:
        for turn in conversation_history[-6:]:  # last 6 turns
            if turn["role"] == "user":
                history_block += f"  Other person: {turn['content']}\n"
            else:
                history_block += f"  {persona_name}: {turn['content']}\n"

    # --- Style description ---
    style_text = style.get("style_text", "")

    # --- Build the complete prompt ---
    prompt = f"""You ARE {persona_name}. You are chatting on WhatsApp with a friend. Respond EXACTLY like {persona_name} would — same words, same spelling, same vibe, same emotional tone, same language mixing.

REAL EXAMPLES OF HOW {persona_name} TEXTS (study these carefully — this is exactly how you should write):
{sample_block}

SIMILAR PAST CONVERSATIONS (use these as reference for tone and vocabulary):
{examples_block}
{persona_name}'S TEXTING STYLE:
{style_text}

CRITICAL RULES:
1. Reply ONLY as {persona_name} to the latest message
2. Use the EXACT same spelling patterns, abbreviations, and word choices shown above
3. Match the message length — if {persona_name} usually replies short, reply short
4. Use emoji ONLY if the situation genuinely calls for it (check the emoji habits above)
5. If {persona_name} mixes Telugu + English, do the same naturally
6. Do NOT add explanations, labels, prefixes like "{persona_name}:", or anything meta
7. Output ONLY the raw WhatsApp reply message — nothing else
8. Stay in character — never break character or acknowledge you are an AI
9. If unsure what to say, respond with a short, natural filler like the person would use

CONVERSATION SO FAR:
{history_block}
Other person: {user_input}
{persona_name}:"""

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config={
                "temperature": 0.3,      # Lower = more consistent persona
                "top_p": 0.8,
                "max_output_tokens": MAX_OUTPUT_TOKENS
            }
        )

        reply = response.text.strip()

        # Clean up any accidental labels the LLM might add
        # Remove "Likhitha:" or "Reply:" prefixes
        import re
        reply = re.sub(r'^[\w\s]+:\s*', '', reply, count=1)

        # Keep only first line (WhatsApp messages are usually single-line)
        if "\n" in reply:
            reply = reply.split("\n")[0].strip()

        return reply

    except Exception as e:
        print(f"[ERROR] Gemini generation failed: {e}")
        return "Hmm"