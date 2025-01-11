import re

punct = {'💁', '[', '’', '~', '💪', '📚', '🏡', '-', '🐣', '🇺', '”', '̶', '\u200a', ';', '🍕', ' ', '!', '%', ',', '👇', '®', '🌈', '?', '🏽', '=', '💨', '✅', '✔', ')', '|', '‘', '\xa0', '🗽', '&', '🏼', '¿', '…', '🎓', '👉', '❌', '🎧', '👈', '🚂', '+', '🤖', '👎', '→', '¡', '🤔', '️', '👸', '@', '🇸', ':', '“', '•', '🏿', '🏻', '👀', '👏', '—', ']', '✓', '"', '\u200b', '🎤', '\n', '.', '(', '$', '❤', '⬇', '#', '👍', "'", '/', '*', '🏾', '–', '👿'}

punct.remove(' ')  # keep spaces
punct.remove('#')  # keep hashtags
punct.remove('@')  # keep mentions
punct.remove('\'') # keep single quotes (in order to retain I'm, isn't, etc.)

def clean(text):
    temp_text = text.lower()
    temp_text = re.sub(r'https?://\S+', '', temp_text)
    temp_text = re.sub(r'\d+', '0', temp_text)
    temp_text = temp_text.replace('’', '\'')  # some single quotes are slanted, and we want to retain them
    for p in punct:
        temp_text = temp_text.replace(p, ' ')
    temp_text = re.sub(r'\s+', ' ', temp_text)
    cleaned_text = temp_text.strip()
    return cleaned_text