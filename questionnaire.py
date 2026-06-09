"""
Questionnaire-based persona builder.

Asks the user interactive questions to build the same style profile dict
that style_analyzer.style_summary() returns from chat analysis.
This allows persona creation without a WhatsApp chat export.
"""


def run_questionnaire():
    """
    Run an interactive questionnaire and return (persona_name, style_dict).
    The style_dict has the same keys as style_summary() output.
    """
    print("\n" + "=" * 55)
    print("  PERSONA QUESTIONNAIRE")
    print("  Answer these questions about the person you want to clone.")
    print("=" * 55 + "\n")

    # --- Persona name ---
    persona_name = input("1. What is this person's name? ").strip()
    if not persona_name:
        print("Name is required!")
        exit()

    # --- Message length ---
    print(f"\n2. How long are {persona_name}'s typical messages?")
    print("   1) Very short (1-4 words, like 'ok', 'hmm', 'yeah sure')")
    print("   2) Short to medium (5-8 words)")
    print("   3) Medium to long (9+ words)")
    length_choice = input("   Choose [1/2/3]: ").strip()

    if length_choice == "1":
        avg_words = 3.0
    elif length_choice == "3":
        avg_words = 12.0
    else:
        avg_words = 6.0

    # --- Short reply ratio ---
    print(f"\n3. How often does {persona_name} send very short replies (3 words or less)?")
    print("   1) Most of the time (>60%)")
    print("   2) About half the time (~40-60%)")
    print("   3) Sometimes (~20-40%)")
    print("   4) Rarely (<20%)")
    short_choice = input("   Choose [1/2/3/4]: ").strip()

    short_ratio_map = {"1": 0.7, "2": 0.5, "3": 0.3, "4": 0.1}
    short_ratio = short_ratio_map.get(short_choice, 0.3)

    # --- Capitalization ---
    print(f"\n4. How does {persona_name} handle capitalization?")
    print("   1) Almost always lowercase (no caps at all)")
    print("   2) Mixed — sometimes lowercase, sometimes normal")
    print("   3) Normal capitalization (proper sentences)")
    cap_choice = input("   Choose [1/2/3]: ").strip()

    if cap_choice == "1":
        lower_ratio = 0.9
    elif cap_choice == "3":
        lower_ratio = 0.1
    else:
        lower_ratio = 0.5

    # --- Emoji usage frequency ---
    print(f"\n5. How often does {persona_name} use emojis?")
    print("   1) Very frequently (in most messages)")
    print("   2) Sometimes (in about 30-50% of messages)")
    print("   3) Occasionally (once every few messages)")
    print("   4) Rarely or never")
    emoji_choice = input("   Choose [1/2/3/4]: ").strip()

    emoji_ratio_map = {"1": 0.7, "2": 0.4, "3": 0.15, "4": 0.02}
    emoji_ratio = emoji_ratio_map.get(emoji_choice, 0.15)

    # --- Favorite emojis ---
    common_emojis = []
    if emoji_ratio > 0.05:
        emoji_input = input(
            f"\n6. What emojis does {persona_name} use most? "
            "(Type them separated by spaces, e.g., 😂 🙂 ❤️): "
        ).strip()
        if emoji_input:
            common_emojis = emoji_input.split()[:5]
    else:
        print(f"\n6. Skipped (rarely uses emojis)")

    # --- Question asking ---
    print(f"\n7. Does {persona_name} ask questions back in conversations?")
    print("   1) Often (curious, engages a lot)")
    print("   2) Sometimes")
    print("   3) Rarely (mostly just answers)")
    question_choice = input("   Choose [1/2/3]: ").strip()

    question_ratio_map = {"1": 0.4, "2": 0.2, "3": 0.05}
    question_ratio = question_ratio_map.get(question_choice, 0.2)

    # --- Exclamation marks ---
    print(f"\n8. Does {persona_name} use exclamation marks (!)?")
    print("   1) Often")
    print("   2) Sometimes")
    print("   3) Rarely")
    exclaim_choice = input("   Choose [1/2/3]: ").strip()

    exclaim_ratio_map = {"1": 0.3, "2": 0.15, "3": 0.03}
    exclaim_ratio = exclaim_ratio_map.get(exclaim_choice, 0.15)

    # --- Ellipsis ---
    print(f"\n9. Does {persona_name} use '...' in messages?")
    print("   1) Yes, often")
    print("   2) Sometimes")
    print("   3) Rarely or never")
    ellipsis_choice = input("   Choose [1/2/3]: ").strip()

    ellipsis_ratio_map = {"1": 0.35, "2": 0.15, "3": 0.02}
    ellipsis_ratio = ellipsis_ratio_map.get(ellipsis_choice, 0.02)

    # --- Chat language (multilingual) ---
    print(f"\n10. What language does {persona_name} primarily chat in?")
    print("    (besides English — e.g., Hindi, Telugu, Tamil, Kannada, Bengali, Marathi, etc.)")
    print("    Type the language name, or 'english' if they only use English.")
    chat_language_input = input("    Language: ").strip()

    chat_language = None
    native_words = []

    if chat_language_input.lower() not in ("english", "eng", "en", ""):
        chat_language = chat_language_input.capitalize()

        native_words_input = input(
            f"    Enter common {chat_language} words/phrases {persona_name} uses\n"
            f"    (comma separated, e.g., for Hindi: kya, hai, nahi, accha, yaar): "
        ).strip()
        if native_words_input:
            native_words = [w.strip() for w in native_words_input.split(",") if w.strip()][:15]

    # --- Nicknames ---
    print(f"\n11. Does {persona_name} call you (or others) by any nickname or address term?")
    print("    (e.g., bro, ra, anna, bhai, macha, dude, boss, etc.)")
    nicknames_input = input(
        "    Enter nicknames they use (comma separated, or press Enter to skip): "
    ).strip()

    nicknames = []
    nickname_freq = {}
    if nicknames_input:
        nicknames = [n.strip() for n in nicknames_input.split(",") if n.strip()][:8]

        print(f"\n12. How frequently does {persona_name} use these nicknames?")
        print("    1) Very often (almost every message)")
        print("    2) Sometimes (every few messages)")
        print("    3) Occasionally (once in a while)")
        nick_freq_choice = input("    Choose [1/2/3]: ").strip()

        # Set a representative frequency count
        freq_map = {"1": 50, "2": 20, "3": 5}
        freq_val = freq_map.get(nick_freq_choice, 20)
        nickname_freq = {n: freq_val for n in nicknames}
    else:
        print("\n12. Skipped (no nicknames)")

    # --- Common words / slang ---
    print(f"\n13. What other words, slang, or phrases does {persona_name} use often?")
    words_input = input(
        "    (comma separated, e.g., lol, nah, bruh, yep, hmm): "
    ).strip()
    common_words = []
    if words_input:
        common_words = [w.strip() for w in words_input.split(",") if w.strip()][:15]

    # --- Multiple messages in a row ---
    print(f"\n14. Does {persona_name} send multiple short messages in a row")
    print("    instead of one long message?")
    multi_choice = input("    (yes/no): ").strip().lower()
    sends_multiple = multi_choice in ("yes", "y")

    # --- Conversation initiation ---
    print(f"\n15. Does {persona_name} usually start conversations or mostly just reply?")
    print("   1) Often starts conversations")
    print("   2) Sometimes starts, sometimes replies")
    print("   3) Mostly just replies to others")
    init_choice = input("   Choose [1/2/3]: ").strip()
    initiates_convo = init_choice in ("1", "2")

    # --- Sample messages ---
    print(f"\n16. Provide 3-5 example messages showing how {persona_name} actually texts.")
    print("    (Type one per line. Press Enter on a blank line when done)")

    samples = []
    while len(samples) < 8:
        sample = input(f"    Example {len(samples) + 1}: ").strip()
        if not sample:
            break
        samples.append(sample)

    if not samples:
        print("    (No samples provided — the AI will rely on the style profile only)")

    # --- Build the style dict (same structure as style_summary() output) ---
    style_lines = []

    if avg_words <= 4:
        style_lines.append(f"Sends very short messages, usually 1-4 words (avg {avg_words:.1f} words).")
    elif avg_words <= 8:
        style_lines.append(f"Sends short to medium messages (avg {avg_words:.1f} words).")
    else:
        style_lines.append(f"Sends medium to long messages (avg {avg_words:.1f} words).")

    if short_ratio > 0.5:
        style_lines.append(f"{int(short_ratio*100)}% of replies are 3 words or less — very terse replier.")

    if lower_ratio > 0.7:
        style_lines.append("Almost never uses capital letters — all lowercase style.")
    elif lower_ratio > 0.4:
        style_lines.append("Mixes lowercase and normal capitalization.")

    if emoji_ratio > 0.4:
        style_lines.append(f"Uses emojis frequently (in ~{int(emoji_ratio*100)}% of messages).")
    elif emoji_ratio > 0.1:
        style_lines.append(f"Uses emojis sometimes (in ~{int(emoji_ratio*100)}% of messages).")
    else:
        style_lines.append("Rarely uses emojis.")

    if common_emojis:
        style_lines.append(f"Favorite emojis: {' '.join(common_emojis[:5])}")
        style_lines.append("Only use an emoji if the situation naturally calls for it. Never force emojis.")

    if question_ratio > 0.2:
        style_lines.append("Often asks questions back in conversation.")

    if exclaim_ratio > 0.2:
        style_lines.append("Uses exclamation marks fairly often.")
    elif exclaim_ratio < 0.05:
        style_lines.append("Rarely uses exclamation marks.")

    if ellipsis_ratio > 0.1:
        style_lines.append("Sometimes uses '...' in messages.")

    # Language info (multilingual)
    if chat_language and native_words:
        style_lines.append(f"Chats in {chat_language} transliteration mixed with English (code-switching).")
        style_lines.append(f"Common {chat_language} words used: {', '.join(native_words[:10])}.")
        style_lines.append(f"IMPORTANT: Respond in {chat_language} transliteration + English mix, matching the person's style.")
    elif chat_language:
        style_lines.append(f"Chats in {chat_language} mixed with English.")
        style_lines.append(f"IMPORTANT: Respond in {chat_language} transliteration + English mix.")

    # Nickname info
    if nicknames:
        nick_parts = []
        for nick in nicknames[:5]:
            freq = nickname_freq.get(nick, 0)
            if freq >= 50:
                nick_parts.append(f"'{nick}' (very often)")
            elif freq >= 20:
                nick_parts.append(f"'{nick}' (sometimes)")
            else:
                nick_parts.append(f"'{nick}' (occasionally)")
        style_lines.append(f"Uses these nicknames/address terms: {', '.join(nick_parts)}.")
        style_lines.append(f"Use these nicknames naturally in replies when addressing the other person.")

    if common_words:
        style_lines.append(f"Frequently used words: {', '.join(common_words[:10])}.")

    if sends_multiple:
        style_lines.append("Often sends 2-3 short messages in a row instead of one long one.")

    if initiates_convo:
        style_lines.append("Sometimes initiates conversations, not just reactive.")
    else:
        style_lines.append("Mostly responds to others, rarely starts conversations unprompted.")

    style_text = "\n".join(f"- {line}" for line in style_lines)

    style = {
        "style_text": style_text,
        "sample_messages": samples,
        "common_emojis": common_emojis,
        "avg_words": avg_words,
        "short_ratio": short_ratio,
        "emoji_ratio": emoji_ratio,
        "chat_language": chat_language,
        "native_words": native_words,
        "nicknames": nicknames,
        "nickname_freq": nickname_freq,
        "common_words": common_words,
        "length_stats": {
            "avg_words": avg_words,
            "short_reply_ratio": short_ratio,
        },
        "punctuation_style": {
            "all_lower_ratio": lower_ratio,
            "question_ratio": question_ratio,
            "exclaim_ratio": exclaim_ratio,
            "ellipsis_ratio": ellipsis_ratio,
        },
        "conversation_style": {
            "initiates_convo": initiates_convo,
            "sends_multiple_msgs": sends_multiple,
        },
        "emoji_usage_ratio": emoji_ratio,
        "actual_word_forms": common_words,
    }

    print(f"\n{'=' * 55}")
    print(f"  Persona profile for {persona_name} built!")
    print(f"{'=' * 55}")
    print(f"\n{style_text}\n")

    return persona_name, style
