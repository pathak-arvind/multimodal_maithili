from collections import defaultdict

# Function to build bigram frequency from a text file
def build_bigram_freq(filename):
    """Builds a dictionary of bigram frequencies from the given file."""
    bigram_map = defaultdict(int)
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for word in file.read().split():
                for i in range(len(word) - 1):
                    bigram = word[i:i+2]
                    bigram_map[bigram] += 1
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
    return bigram_map

# Function to identify language using bigram score
def identify_language(word, eng_bigrams, maithili_bigrams):
    """Identify the language of a word using bigram scores."""
    eng_score = 0
    maithili_score = 0

    for i in range(len(word) - 1):
        bigram = word[i:i+2]
        if bigram in eng_bigrams:
            eng_score += eng_bigrams[bigram]
        if bigram in maithili_bigrams:
            maithili_score += maithili_bigrams[bigram]

    if eng_score > maithili_score:
        return "English"
    elif maithili_score > eng_score:
        return "Maithili"
    else:
        return "Unknown"

# ✅ Function for UI to directly call with input_text
def process_mixed_corpus(input_text):
    """Takes a string and classifies each word as English or Maithili."""
    eng_bigrams = build_bigram_freq("eng_corpus.txt")
    maithili_bigrams = build_bigram_freq("maithili_corpus.txt")

    if not eng_bigrams or not maithili_bigrams:
        return ["Error: Could not load one or both corpus files."]

    results = []
    for word in input_text.split():
        lang = identify_language(word, eng_bigrams, maithili_bigrams)
        results.append(f"{word}: {lang}")

    return results
