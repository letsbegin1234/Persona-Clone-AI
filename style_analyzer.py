import emoji
import re
from collections import Counter


# Multilingual transliteration patterns — maps language name to common patterns
LANGUAGE_PATTERNS = {
    "Telugu": [
        'undi', 'undhi', 'ante', 'kadha', 'enti', 'chala', 'baaga',
        'ledu', 'ledhu', 'avunu', 'kaadu', 'mari', 'inka', 'chesth',
        'velli', 'vacch', 'untey', 'aithe', 'chepp', 'cheyy',
        'manchi', 'bagundh', 'anna', 'akka', 'ohhh', 'haa', 'haaa',
        'emo', 'ala', 'ela', 'entha', 'endh', 'eppu', 'ikka',
        'poyav', 'vachav', 'unnav', 'chesav', 'tinn', 'padd',
        'nuvvu', 'meeru', 'naaku', 'vaadu', 'thinu', 'raave',
    ],
    "Hindi": [
        'kya', 'hai', 'nahi', 'yaar', 'bhai', 'accha', 'theek',
        'kaise', 'kaisa', 'kahan', 'kab', 'kyun', 'abhi', 'bahut',
        'acha', 'achha', 'mujhe', 'tujhe', 'haan', 'sahi', 'chal',
        'chalo', 'dekh', 'bata', 'bol', 'sun', 'ruk', 'aaja',
        'jaana', 'karna', 'hota', 'wala', 'waala', 'kuch', 'aur',
        'lekin', 'matlab', 'samajh', 'pata', 'mast', 'soch',
        'dosti', 'pyaar', 'arre', 'oye', 'pakka', 'bilkul',
    ],
    "Tamil": [
        'enna', 'illa', 'poda', 'podi', 'vaanga', 'sollu', 'pannunga',
        'romba', 'konjam', 'thaan', 'irukku', 'iruku', 'varuvom',
        'panna', 'solla', 'kelunga', 'theriyum', 'therla', 'innum',
        'epdi', 'enga', 'yenna', 'ippo', 'appuram', 'pogalaam',
        'nanba', 'macha', 'thala', 'vanakkam', 'nandri',
    ],
    "Kannada": [
        'enu', 'hege', 'illi', 'alli', 'baa', 'baro', 'maadi',
        'hogi', 'bandu', 'nodri', 'gottu', 'gottilla', 'chennaag',
        'thumba', 'yavag', 'yelli', 'yaak', 'houdu', 'illa',
        'guru', 'maga', 'machha', 'swalpa', 'nimdu', 'nange',
    ],
    "Bengali": [
        'kemon', 'achi', 'acho', 'bhalo', 'kothay', 'keno',
        'bolo', 'jao', 'eso', 'koro', 'bolchi', 'janona',
        'hobe', 'korbo', 'jabo', 'khabo', 'dada', 'didi',
        'ekhane', 'okhane', 'kichu', 'shob', 'amake', 'tomake',
    ],
    "Marathi": [
        'kay', 'aahe', 'nahi', 'kasa', 'kashi', 'kuthe', 'keva',
        'mala', 'tula', 'tyala', 'yeto', 'jato', 'karto', 'bola',
        'baghto', 'zala', 'hota', 'nako', 'chya', 'rao',
    ],
    "Malayalam": [
        'enna', 'illa', 'und', 'varu', 'podu', 'aano', 'cheyyuka',
        'enthu', 'evide', 'ini', 'ippo', 'sheriyaan', 'mathi',
        'machane', 'chetta', 'chechi', 'potte', 'adipoli',
    ],
    "Gujarati": [
        'kem', 'cho', 'haa', 'naa', 'shu', 'kyaan', 'aavu',
        'karo', 'jaav', 'bolo', 'samju', 'bhai', 'yaar',
        'majama', 'chalse', 'thayyu', 'karisu',
    ],
    "Punjabi": [
        'ki', 'haal', 'paaji', 'veere', 'kiven', 'kiddan',
        'changa', 'theek', 'nahi', 'oye', 'karo', 'jao',
        'dekho', 'suno', 'billo', 'vadiya',
    ],
}

# Common nicknames / address terms across Indian languages
NICKNAME_PATTERNS = [
    'bro', 'bruh', 'bhai', 'bhaiya', 'yaar', 'dude', 'man',
    'ra', 're', 'da', 'di', 'anna', 'akka', 'mama', 'mawa',
    'macha', 'machha', 'machan', 'machane', 'guru', 'boss',
    'dada', 'didi', 'chetta', 'chechi', 'paaji', 'veere',
    'nanba', 'thala', 'oye', 'arre', 'abey', 'abe',
    'buddy', 'fam', 'mate', 'homie', 'dost', 'maga',
    'sir', 'maam', 'ji',
]


def detect_languages(messages):
    """
    Detect which language(s) are used in the messages by matching
    transliteration patterns. Returns a list of (language, score, matched_words).
    """
    language_scores = {}
    language_words = {}

    for lang, patterns in LANGUAGE_PATTERNS.items():
        matched = set()
        for m in messages:
            words = re.findall(r'[a-zA-Z]+', m.lower())
            for w in words:
                for pattern in patterns:
                    if pattern in w:
                        matched.add(w)
                        break

        if matched:
            language_scores[lang] = len(matched)
            language_words[lang] = list(matched)

    # Sort by number of matched words (most likely language first)
    results = []
    for lang in sorted(language_scores, key=language_scores.get, reverse=True):
        results.append((lang, language_scores[lang], language_words[lang][:15]))

    return results


def detect_nicknames(messages):
    """
    Detect common nicknames/address terms used in messages.
    Looks for words that appear at the start or end of messages frequently.
    Returns list of (nickname, count) sorted by frequency.
    """
    nickname_counter = Counter()

    for m in messages:
        words = re.findall(r'[a-zA-Z]+', m.lower())
        if not words:
            continue

        # Check first and last words against known nickname patterns
        for w in [words[0], words[-1]] if len(words) > 1 else [words[0]]:
            if w in NICKNAME_PATTERNS or any(p == w for p in NICKNAME_PATTERNS):
                nickname_counter[w] += 1

        # Also check all words but only count if they're short address terms
        for w in words:
            if w in NICKNAME_PATTERNS and len(w) <= 5:
                nickname_counter[w] += 1

    # Return nicknames that appear at least 3 times
    results = [(nick, count) for nick, count in nickname_counter.most_common(10)
               if count >= 3]

    return results


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

    # --- Multilingual transliteration detection ---
    detected_langs = detect_languages(messages)
    chat_language = None
    native_words = []

    if detected_langs:
        # Use the top detected language
        chat_language = detected_langs[0][0]
        native_words = detected_langs[0][2]

    # --- Nickname detection ---
    detected_nicknames = detect_nicknames(messages)
    nicknames = [nick for nick, count in detected_nicknames]
    nickname_freq = {nick: count for nick, count in detected_nicknames}

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

    # Language-specific info (multilingual)
    if chat_language and native_words:
        style_lines.append(f"Chats in {chat_language} transliteration mixed with English (code-switching).")
        style_lines.append(f"Common {chat_language} words used: {', '.join(native_words[:10])}.")
        style_lines.append(f"IMPORTANT: Respond in {chat_language} transliteration + English mix, matching the person's style.")

    # Nickname info
    if nicknames:
        nick_parts = []
        for nick in nicknames[:5]:
            freq = nickname_freq.get(nick, 0)
            nick_parts.append(f"'{nick}' ({freq}x)")
        style_lines.append(f"Uses these nicknames/address terms: {', '.join(nick_parts)}.")
        style_lines.append(f"Use these nicknames naturally in replies when addressing the other person.")

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
        "chat_language": chat_language,
        "native_words": native_words,
        "nicknames": nicknames,
        "nickname_freq": nickname_freq,
        "common_words": common_words,
    }