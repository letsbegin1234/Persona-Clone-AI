import emoji
import re
from collections import Counter


def style_summary(messages):
    """
    Analyze the target person's messages to build a comprehensive style profile.
    Returns a dict with style characteristics AND a formatted string for the LLM.
    """
    if not messages:
        return {"style_text": "No style data available.", "sample_messages": []}

    # --- Message length analysis ---
    word_counts = [len(m.split()) for m in messages]
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 5
    short_replies = sum(1 for wc in word_counts if wc <= 3)
    short_ratio = short_replies / len(messages) if messages else 0

    # --- Emoji analysis ---
    emoji_msgs = 0
    all_emojis = []
    for m in messages:
        msg_emojis = [c for c in m if c in emoji.EMOJI_DATA]
        if msg_emojis:
            emoji_msgs += 1
            all_emojis.extend(msg_emojis)

    emoji_ratio = emoji_msgs / len(messages) if messages else 0
    common_emojis = [e for e, _ in Counter(all_emojis).most_common(5)]

    # --- Capitalization analysis ---
    all_lower = sum(1 for m in messages if m == m.lower())
    lower_ratio = all_lower / len(messages) if messages else 0

    # --- Punctuation analysis ---
    question_msgs = sum(1 for m in messages if "?" in m)
    exclaim_msgs = sum(1 for m in messages if "!" in m)
    ellipsis_msgs = sum(1 for m in messages if "..." in m)
    question_ratio = question_msgs / len(messages) if messages else 0

    # --- Common words (excluding very short/common ones) ---
    all_words = []
    for m in messages:
        words = re.findall(r'[a-zA-Z]+', m.lower())
        all_words.extend(w for w in words if len(w) > 2)

    word_freq = Counter(all_words)
    # Remove very common English words
    stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all',
                  'can', 'had', 'her', 'was', 'one', 'our', 'out', 'has',
                  'have', 'that', 'this', 'with', 'from', 'they', 'will'}
    common_words = [w for w, c in word_freq.most_common(30)
                    if w not in stop_words and c >= 2][:15]

    # --- Telugu transliteration detection ---
    # Common Telugu transliteration patterns
    telugu_patterns = [
        'undi', 'undhi', 'ante', 'kadha', 'enti', 'chala', 'baaga',
        'ledu', 'ledhu', 'avunu', 'kaadu', 'mari', 'inka', 'chesth',
        'velli', 'vacch', 'untey', 'aithe', 'chepp', 'cheyy',
        'manchi', 'bagundh', 'anna', 'akka', 'ohhh', 'haa', 'haaa',
        'emo', 'ala', 'ela', 'entha', 'endh', 'eppu', 'ikka',
        'poyav', 'vachav', 'unnav', 'chesav', 'tinn', 'padd',
    ]
    telugu_words_found = set()
    for m in messages:
        words = re.findall(r'[a-zA-Z]+', m.lower())
        for w in words:
            for pattern in telugu_patterns:
                if pattern in w:
                    telugu_words_found.add(w)
                    break

    telugu_words = list(telugu_words_found)[:12]

    # --- Sample messages (real examples for few-shot) ---
    # Pick diverse samples: short, medium, with emoji, questions
    samples = []
    short_samples = [m for m in messages if len(m.split()) <= 3]
    medium_samples = [m for m in messages if 3 < len(m.split()) <= 8]
    emoji_samples = [m for m in messages if any(c in emoji.EMOJI_DATA for c in m)]
    question_samples = [m for m in messages if "?" in m]

    # Take a mix
    for group in [short_samples, medium_samples, emoji_samples, question_samples]:
        for m in group[:3]:
            if m not in samples:
                samples.append(m)
            if len(samples) >= 10:
                break

    # --- Build human-readable style description ---
    style_lines = []

    if avg_words <= 4:
        style_lines.append(f"Sends very short messages, usually 1-4 words (avg {avg_words:.1f} words).")
    elif avg_words <= 8:
        style_lines.append(f"Sends short to medium messages (avg {avg_words:.1f} words).")
    else:
        style_lines.append(f"Sends medium length messages (avg {avg_words:.1f} words).")

    if short_ratio > 0.5:
        style_lines.append(f"{int(short_ratio*100)}% of replies are 3 words or less — very terse replier.")

    if lower_ratio > 0.7:
        style_lines.append("Almost never uses capital letters — all lowercase style.")
    elif lower_ratio > 0.4:
        style_lines.append("Mixes lowercase and normal capitalization.")

    if emoji_ratio > 0.4:
        style_lines.append(f"Uses emojis frequently (in ~{int(emoji_ratio*100)}% of messages).")
    elif emoji_ratio > 0.15:
        style_lines.append(f"Uses emojis sometimes (in ~{int(emoji_ratio*100)}% of messages).")
    else:
        style_lines.append("Rarely uses emojis.")

    if common_emojis:
        style_lines.append(f"Favorite emojis: {' '.join(common_emojis[:5])}")
        style_lines.append("Only use an emoji if the situation naturally calls for it. Never force emojis.")

    if question_ratio > 0.2:
        style_lines.append("Often asks questions back in conversation.")

    if telugu_words:
        style_lines.append(f"Uses Telugu transliteration words like: {', '.join(telugu_words[:8])}.")
        style_lines.append("Mixes Telugu transliteration and English naturally (code-switching).")

    if common_words:
        style_lines.append(f"Frequently used words: {', '.join(common_words[:10])}.")

    style_text = "\n".join(f"- {line}" for line in style_lines)

    return {
        "style_text": style_text,
        "sample_messages": samples,
        "common_emojis": common_emojis,
        "avg_words": avg_words,
        "short_ratio": short_ratio,
        "emoji_ratio": emoji_ratio,
        "telugu_words": telugu_words,
        "common_words": common_words,
    }