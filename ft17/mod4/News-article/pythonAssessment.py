"""
pythonAssessment.py
--------------------
NLP News Article Analyzer
Performs text analysis on a given news article, including:
  - Counting occurrences of a specific word
  - Identifying the most common word
  - Calculating the average word length
  - Counting paragraphs
  - Counting sentences
"""

import re
from collections import Counter


# ---------------------------------------------------------------------------
# 1. Count Specific Word
# ---------------------------------------------------------------------------

def count_specific_word(text: str, word: str) -> int:
    """
    Count the number of times a specific word appears in the text.

    Matching is case-insensitive and whole-word only (e.g. searching for
    "pie" won't match "pies").

    Args:
        text (str): The text to search through.
        word (str): The word to search for.

    Returns:
        int: Number of occurrences. Returns 0 if no matches are found.
    """
    if not text or not word:
        return 0

    # \b ensures whole-word matching; re.IGNORECASE makes it case-insensitive
    pattern = r'\b' + re.escape(word) + r'\b'
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return len(matches)


# ---------------------------------------------------------------------------
# 2. Identify Most Common Word
# ---------------------------------------------------------------------------

def identify_most_common_word(text: str) -> str | None:
    """
    Identify the most frequently occurring word in the text.

    Punctuation is stripped and comparison is case-insensitive so that
    "Baking" and "baking" are treated as the same word.

    Args:
        text (str): The text to analyse.

    Returns:
        str | None: The most common word (lowercased), or None if the text
                    is empty.
    """
    if not text.strip():
        return None

    # Extract only alphabetic tokens (strips punctuation automatically)
    words = re.findall(r"[a-zA-Z']+", text.lower())

    if not words:
        return None

    word_counts = Counter(words)
    most_common_word, _ = word_counts.most_common(1)[0]
    return most_common_word


# ---------------------------------------------------------------------------
# 3. Calculate Average Word Length
# ---------------------------------------------------------------------------

def calculate_average_word_length(text: str) -> float:
    """
    Calculate the average length of words in the text.

    Punctuation and special characters are excluded from each word before
    its length is measured.

    Args:
        text (str): The text to analyse.

    Returns:
        float: Average word length rounded to 2 decimal places.
               Returns 0 if the text is empty.
    """
    if not text.strip():
        return 0

    # Pull out only alphabetic sequences (no digits, no punctuation)
    words = re.findall(r"[a-zA-Z]+", text)

    if not words:
        return 0

    total_length = 0
    for word in words:
        total_length += len(word)

    average = total_length / len(words)
    return round(average, 2)


# ---------------------------------------------------------------------------
# 4. Count Paragraphs
# ---------------------------------------------------------------------------

def count_paragraphs(text: str) -> int:
    """
    Count the number of paragraphs in the text.

    Paragraphs are defined as blocks of text separated by one or more
    blank lines.

    Args:
        text (str): The text to analyse.

    Returns:
        int: Number of paragraphs. Returns 1 for an empty string.
    """
    if not text.strip():
        return 1

    # Split on one-or-more blank lines; filter out empty chunks
    paragraphs = re.split(r'\n\s*\n', text.strip())
    non_empty = [p for p in paragraphs if p.strip()]
    return len(non_empty)


# ---------------------------------------------------------------------------
# 5. Count Sentences
# ---------------------------------------------------------------------------

def count_sentences(text: str) -> int:
    """
    Count the number of sentences in the text.

    Sentences are delimited by '.', '!' or '?' characters.

    Args:
        text (str): The text to analyse.

    Returns:
        int: Number of sentences. Returns 1 for an empty string.
    """
    if not text.strip():
        return 1

    # Split on sentence-ending punctuation followed by optional whitespace
    sentences = re.split(r'[.!?]+', text.strip())
    non_empty = [s for s in sentences if s.strip()]
    return len(non_empty)


# ---------------------------------------------------------------------------
# Main script
# ---------------------------------------------------------------------------

def main():
    # --- Read the article from file ---
    file_path = "article.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        article_text = file.read()

    print("=" * 60)
    print("        NLP News Article Analyzer")
    print("=" * 60)
    print(f"\nArticle loaded from: {file_path}\n")

    # --- 1. Count a specific word (while loop for multiple queries) ---
    search_words = ["apple", "machine", "baking", "technology", "pie"]
    index = 0

    print("-" * 60)
    print("1. SPECIFIC WORD COUNTS")
    print("-" * 60)

    while index < len(search_words):
        word = search_words[index]
        count = count_specific_word(article_text, word)
        print(f"   '{word}' appears {count} time(s) in the article.")
        index += 1

    # --- 2. Most common word ---
    print("\n" + "-" * 60)
    print("2. MOST COMMON WORD")
    print("-" * 60)

    most_common = identify_most_common_word(article_text)

    if most_common is not None:
        print(f"   The most common word is: '{most_common}'")
    else:
        print("   The text is empty — no common word found.")

    # --- 3. Average word length (for loop to show per-paragraph stats) ---
    print("\n" + "-" * 60)
    print("3. AVERAGE WORD LENGTH")
    print("-" * 60)

    avg_length = calculate_average_word_length(article_text)
    print(f"   Average word length across the full article: {avg_length} characters")

    # Show average word length per paragraph using a for loop
    paragraphs = re.split(r'\n\s*\n', article_text.strip())
    non_empty_paragraphs = [p for p in paragraphs if p.strip()]

    print("\n   Per-paragraph breakdown:")
    for i, paragraph in enumerate(non_empty_paragraphs, start=1):
        para_avg = calculate_average_word_length(paragraph)
        # Truncate long paragraphs for display
        preview = paragraph.strip()[:55].replace('\n', ' ')
        print(f"   Paragraph {i:>2} | Avg word length: {para_avg} | Preview: \"{preview}...\"")

    # --- 4. Count paragraphs ---
    print("\n" + "-" * 60)
    print("4. PARAGRAPH COUNT")
    print("-" * 60)

    paragraph_count = count_paragraphs(article_text)
    print(f"   Total number of paragraphs: {paragraph_count}")

    # --- 5. Count sentences ---
    print("\n" + "-" * 60)
    print("5. SENTENCE COUNT")
    print("-" * 60)

    sentence_count = count_sentences(article_text)
    print(f"   Total number of sentences: {sentence_count}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Most common word  : '{most_common}'")
    print(f"  Avg word length   : {avg_length} characters")
    print(f"  Total paragraphs  : {paragraph_count}")
    print(f"  Total sentences   : {sentence_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()