import re


def parse_chat(file_path, target_person):
    """
    Parse WhatsApp chat export and extract:
    - messages: all messages from the target person
    - pairs: (context_window, reply) tuples with multi-message context
    - full_chat: all (person, message) tuples
    """
    messages = []
    pairs = []
    full_chat = []

    pattern = r"^\d{1,2}/\d{1,2}/\d{2,4},"

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Merge multi-line messages
    chats = []
    current = ""

    for line in lines:
        if re.match(pattern, line):
            if current:
                chats.append(current)
            current = line.strip()
        else:
            current += " " + line.strip()

    if current:
        chats.append(current)

    # Extract (person, message) tuples
    for chat in chats:
        parts = chat.split(" - ", 1)
        if len(parts) < 2:
            continue

        message_part = parts[1]
        if ":" not in message_part:
            continue

        person, message = message_part.split(":", 1)
        person = person.strip()
        message = message.strip()

        if "<Media omitted>" in message or not message:
            continue

        # Skip system messages and links-only messages
        if "<This message was edited>" in message:
            message = message.replace("<This message was edited>", "").strip()
        if not message:
            continue

        full_chat.append((person, message))

    # Build conversation pairs with context windows
    # Instead of just single Q→A, capture 1-3 preceding messages as context
    for i, (person, message) in enumerate(full_chat):
        if person == target_person:
            messages.append(message)

            # Gather context: collect preceding messages from others
            # (up to 3 messages before the target person's reply)
            context_parts = []
            j = i - 1
            while j >= 0 and len(context_parts) < 3:
                prev_person, prev_msg = full_chat[j]
                if prev_person == target_person:
                    break  # Stop at the target person's previous message
                context_parts.insert(0, prev_msg)
                j -= 1

            if context_parts:
                # Join context messages — this is what the target person
                # was replying to
                context = " | ".join(context_parts)
                pairs.append((context, message))

    return messages, pairs, full_chat