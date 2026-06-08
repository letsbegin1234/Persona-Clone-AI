import google.generativeai as genai
import os
import json


def build_style_description(style: dict) -> str:
    """Convert style dict into a rich natural language description for the prompt."""
    desc = []

    length = style.get("length_stats", {})
    punct = style.get("punctuation_style", {})
    convo = style.get("conversation_style", {})

    # Message length behavior
    avg = length.get("avg_words", 5)
    short_ratio = length.get("short_reply_ratio", 0)
    if avg <= 4:
        desc.append("Sends very short messages, usually 1-4 words.")
    elif avg <= 8:
        desc.append("Sends short to medium messages, typically under 10 words.")
    else:
        desc.append("Sends medium length messages.")

    if short_ratio > 0.5:
        desc.append(f"{int(short_ratio*100)}% of replies are 3 words or less — very terse replier.")

    # Capitalization
    if punct.get("all_lower_ratio", 0) > 0.7:
        desc.append("Almost never uses capital letters — all lowercase style.")

    # Punctuation
    if punct.get("question_ratio", 0) > 0.3:
        desc.append("Frequently asks questions back (engages in conversation).")
    if punct.get("exclaim_ratio", 0) < 0.1:
        desc.append("Rarely uses exclamation marks.")
    if punct.get("ellipsis_ratio", 0) > 0.2:
        desc.append("Sometimes uses '...' in messages.")

    # Emoji usage
    emojis = style.get("common_emojis", [])
    emoji_ratio = style.get("emoji_usage_ratio", 0)

    if emojis:

        if emoji_ratio > 0.6:
            desc.append(
                f"Uses emojis very frequently (in about {int(emoji_ratio*100)}% of messages)."
            )

        elif emoji_ratio > 0.3:
            desc.append(
                f"Uses emojis sometimes (in about {int(emoji_ratio*100)}% of messages)."
            )

        elif emoji_ratio > 0.1:
            desc.append(
                f"Uses emojis occasionally (roughly once every few messages)."
            )

        else:
            desc.append("Rarely uses emojis.")

        desc.append(
            f"When emojis are used they are usually one of: {' '.join(emojis[:5])}."
        )

        desc.append(
            "Only use an emoji if the situation actually fits. Never force emojis."
        )
    else:
        desc.append("Almost never uses emojis.")
    # emojis = style.get("common_emojis", [])
    # emoji_freq = style.get("emoji_frequency", {})
    # emoji_ratio = style.get("emoji_usage_ratio", 0)
    # if emojis:
    #     top_emoji = emojis[0] if emojis else ""
    #     desc.append(f"Uses emojis: {' '.join(emojis[:4])}. Most common is '{top_emoji}'but uses only when the situation actually fits not in every message.")
    #     if punct.get("multi_emoji_ratio", 0) > 0.3:
    #         desc.append("Often uses 2+ emojis together (like 😂😂).")
    #     else:
    #         # desc.append("Uses emojis sparingly — only when something is actually funny or surprising.")
    #         desc.append("Uses emojis sparingly — only as per the situation.") 
    # else:
    #     desc.append("Rarely or never uses emojis.")

    # Conversation initiation
    if convo.get("initiates_convo"):
        desc.append("Sometimes initiates conversations, not just reactive.")
    else:
        desc.append("Mostly responds to others, rarely starts conversations unprompted.")

    if convo.get("sends_multiple_msgs"):
        desc.append(f"Often sends 2-3 short messages in a row instead of one long one.")

    # Telugu transliteration
    telugu = style.get("telugu_words", [])
    if telugu:
        desc.append(f"Uses Telugu transliteration words like: {', '.join(telugu[:8])}.")
        desc.append("Mix of Telugu transliteration and English in the same conversation (code-switching).")

    # Common vocabulary
    words = style.get("common_words", [])
    if words:
        desc.append(f"Frequently used words: {', '.join(words[:12])}.")

    actual_forms = style.get("actual_word_forms", [])
    if actual_forms:
        desc.append(f"Actual spelling forms used: {', '.join(actual_forms[:15])}.")

    return "\n".join(f"- {d}" for d in desc)


def generate_response(context: str, style: dict, conversation_history: list) -> str:
    current_message = conversation_history[-1]["content"]
    style_desc = build_style_description(style)

    # Get 5 real sample messages from the person
    samples = style.get("sample_messages", [])
    sample_block = "\n".join(f'  "{m}"' for m in samples[:8]) if samples else ""

    convo = style.get("conversation_style", {})
    sends_multiple = convo.get("sends_multiple_msgs", False)
    initiates = convo.get("initiates_convo", False)

    model = genai.GenerativeModel('models/gemini-3.1-flash-lite-preview')

    system_prompt = f"""You are roleplaying as a specific person in a WhatsApp chat. Your job is to respond EXACTLY like this person would — same spelling, same vocabulary, same vibe, same emotional tone.

REAL EXAMPLES OF HOW THIS PERSON TEXTS (study these carefully):
{sample_block}

SIMILAR PAST CONVERSATIONS (for context):
{context}

THIS PERSON'S TEXTING STYLE:
{style_desc}

CRITICAL RULES:
1. Reply ONLY to the user's latest message: "{current_message}"
2. Use the EXACT same spelling patterns, abbreviations, and word choices shown in the examples above
3. Match the message length — if they usually reply short, reply short
4. Use emoji ONLY if the situation genuinely calls for it (not every message)
- Prefer these emojis if relevant: {', '.join(style.get("common_emojis", [])[:4])}
5. Write in LOWERCASE if that's their style
6. If they mix Telugu transliteration + English, do the same
7. Do NOT add explanations, labels, or anything meta
8. Output ONLY the WhatsApp reply message — nothing else
{"9. Occasionally ask a follow-up question or keep the convo going if it fits naturally." if initiates else "10. Don't over-initiate — respond naturally without forcing conversation."}
"""

    chat_history = []
    for msg in conversation_history[:-1]:
        role = "model" if msg["role"] == "assistant" else "user"
        chat_history.append({"role": role, "parts": [msg["content"]]})

    chat = model.start_chat(history=chat_history)

    try:
        response = chat.send_message(system_prompt)
        reply = response.text.strip()
        # Clean up any accidental labels like "Alex:" or "Reply:"
        reply = re.sub(r'^[\w\s]+:\s*', '', reply)
        return reply
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {e}")


import re