# Enhanced Roman to Devanagari and Devanagari to Roman Transliteration System

# Roman to Devanagari mappings with more complete character coverage
roman_to_devanagari = {
    # Vowels
    'a': 'अ', 'aa': 'आ', 'i': 'इ', 'ii': 'ई', 'ee': 'ई', 
    'u': 'उ', 'oo': 'ऊ', 'uu': 'ऊ', 'ri': 'ऋ', 'e': 'ए', 
    'ai': 'ऐ', 'o': 'ओ', 'au': 'औ',
    
    # Consonants
    'k': 'क', 'kh': 'ख', 'g': 'ग', 'gh': 'घ', 'ng': 'ङ',
    'ch': 'च', 'chh': 'छ', 'j': 'ज', 'jh': 'झ', 'ny': 'ञ',
    't': 'त', 'th': 'थ', 'd': 'द', 'dh': 'ध', 'n': 'न',
    'p': 'प', 'ph': 'फ', 'b': 'ब', 'bh': 'भ', 'm': 'म',
    'y': 'य', 'r': 'र', 'l': 'ल', 'v': 'व', 'w': 'व',
    'sh': 'श', 's': 'स', 'h': 'ह',
    
    # Retroflex consonants
    'T': 'ट', 'Th': 'ठ', 'D': 'ड', 'Dh': 'ढ', 'N': 'ण',
    
    # Additional consonants
    'ksh': 'क्ष', 'tr': 'त्र', 'gn': 'ज्ञ', 'Sh': 'ष', 'L': 'ळ',
    
    # Special characters
    '.': '।', '..': '॥',
    
    # Diacritics/matras will be handled in the conversion function
}

# Vowel matras (when vowel follows a consonant)
vowel_matras = {
    'a': '', 'aa': 'ा', 'i': 'ि', 'ii': 'ी', 'ee': 'ी',
    'u': 'ु', 'uu': 'ू', 'oo': 'ू', 'ri': 'ृ', 'e': 'े',
    'ai': 'ै', 'o': 'ो', 'au': 'ौ'
}

# Devanagari to Roman mappings
devanagari_to_roman = {
    # Vowels
    'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ii', 'उ': 'u', 'ऊ': 'uu',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au', 'ऋ': 'ri',
    
    # Consonants
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
    'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'ny',
    'ट': 'T', 'ठ': 'Th', 'ड': 'D', 'ढ': 'Dh', 'ण': 'N',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh',
    'ष': 'Sh', 'स': 's', 'ह': 'h', 'ळ': 'L',
    
    # Conjuncts
    'क्ष': 'ksh', 'त्र': 'tr', 'ज्ञ': 'gn',
    
    # Special characters
    '।': '.', '॥': '..',
    'ं': 'n', 'ः': 'h',
    
    # Matras
    'ा': 'aa', 'ि': 'i', 'ी': 'ii', 'ु': 'u', 'ू': 'uu',
    'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', 'ृ': 'ri',
    '्': ''  # halant
}

# Conjuncts (consonant combinations)
conjuncts = {
    'क्ष': 'ksh', 'त्र': 'tr', 'ज्ञ': 'gn'
}

def roman_to_devanagari_transliterate(text):
    """Convert Roman script to Devanagari with proper handling of vowel matras"""
    output = ""
    i = 0
    text = text.lower()  # Convert to lowercase for matching
    
    while i < len(text):
        # Skip spaces and special characters
        if text[i] == ' ' or text[i] in ",.?!-;:\"'()[]{}":
            output += text[i]
            i += 1
            continue
        
        # Check for 3-character matches (like 'chh', 'ksh')
        if i + 2 < len(text) and text[i:i+3] in roman_to_devanagari:
            current_token = text[i:i+3]
            token_length = 3
        # Check for 2-character matches (like 'aa', 'kh', 'gh')
        elif i + 1 < len(text) and text[i:i+2] in roman_to_devanagari:
            current_token = text[i:i+2]
            token_length = 2
        # Check for single character matches
        elif text[i] in roman_to_devanagari:
            current_token = text[i]
            token_length = 1
        # If no match, keep character as-is
        else:
            output += text[i]
            i += 1
            continue
        
        # Process consonant + vowel combinations
        # If current token is a consonant and next token is a vowel
        if (current_token in roman_to_devanagari and 
            current_token not in ['a', 'aa', 'i', 'ii', 'u', 'uu', 'e', 'ai', 'o', 'au', 'ri'] and
            i + token_length < len(text)):
            
            # Check for vowel after the consonant
            next_pos = i + token_length
            
            # Check for 2-character vowels (aa, ii, etc.)
            if next_pos + 1 < len(text) and text[next_pos:next_pos+2] in vowel_matras:
                vowel = text[next_pos:next_pos+2]
                vowel_length = 2
            # Check for single-character vowels (a, i, etc.)
            elif next_pos < len(text) and text[next_pos] in vowel_matras:
                vowel = text[next_pos]
                vowel_length = 1
            else:
                vowel = None
                vowel_length = 0
            
            # Apply the consonant + vowel matra
            if vowel:
                output += roman_to_devanagari[current_token] + vowel_matras[vowel]
                i += token_length + vowel_length
            else:
                # If no vowel follows, add halant (्) for pure consonant unless followed by another consonant
                # Check if next character is a space or the end of the string
                if next_pos >= len(text) or text[next_pos] == ' ' or text[next_pos] in ",.?!-;:\"'()[]{}":
                    # Implicit 'a' sound at the end - just add the consonant
                    output += roman_to_devanagari[current_token]
                else:
                    # Add halant to suppress the inherent 'a' sound
                    output += roman_to_devanagari[current_token] + '्'
                i += token_length
        else:
            # Direct conversion for vowels and other characters
            output += roman_to_devanagari[current_token]
            i += token_length
    
    return output

def devanagari_to_roman_transliterate(text):
    """Convert Devanagari script to Roman with better handling of conjuncts and vowel matras"""
    output = ""
    i = 0
    last_was_consonant = False
    
    while i < len(text):
        # Check for specific conjuncts first (like क्ष, त्र)
        found_conjunct = False
        for conjunct, roman in conjuncts.items():
            if i + len(conjunct) <= len(text) and text[i:i+len(conjunct)] == conjunct:
                output += roman
                i += len(conjunct)
                last_was_consonant = True
                found_conjunct = True
                break
        
        if found_conjunct:
            continue
        
        # Check for halant (consonant without vowel)
        if i + 1 < len(text) and text[i+1] == '्':
            if text[i] in devanagari_to_roman:
                output += devanagari_to_roman[text[i]]
                i += 2  # Skip the consonant and halant
                last_was_consonant = True
                continue
        
        # Handle regular characters
        if text[i] in devanagari_to_roman:
            # If current character is vowel matra and previous output ended with consonant
            if text[i] in 'ािीुूृेैोौं' and last_was_consonant:
                output += devanagari_to_roman[text[i]]
            else:
                # For standalone characters
                output += devanagari_to_roman[text[i]]
                # Reset consonant flag if this is a vowel matra
                last_was_consonant = text[i] not in 'ािीुूृेैोौं'
            i += 1
        else:
            # Keep non-Devanagari characters as is
            output += text[i]
            last_was_consonant = False
            i += 1
    
    return output

def detect_script(text):
    """Detect whether text is predominantly in Devanagari or Roman script"""
    devanagari_count = sum(1 for char in text if ord(char) >= 0x0900 and ord(char) <= 0x097F)
    roman_count = sum(1 for char in text if (ord(char) >= 0x0041 and ord(char) <= 0x005A) or 
                                          (ord(char) >= 0x0061 and ord(char) <= 0x007A))
    
    if devanagari_count > roman_count:
        return 'devanagari'
    else:
        return 'roman'

def text_transliterate(text, direction=None):
    """
    Bidirectional transliteration function with auto-detection.
    
    Args:
        text (str): Text to transliterate
        direction (str, optional): Conversion direction. If None, auto-detects.
                                  Options: 'roman_to_devanagari', 'devanagari_to_roman'
    
    Returns:
        str: Transliterated text
    """
    # Auto-detect if direction is not specified
    if direction is None:
        detected_script = detect_script(text)
        direction = 'devanagari_to_roman' if detected_script == 'devanagari' else 'roman_to_devanagari'
    
    if direction == 'roman_to_devanagari':
        return roman_to_devanagari_transliterate(text)
    elif direction == 'devanagari_to_roman':
        return devanagari_to_roman_transliterate(text)
    else:
        return "Invalid direction. Use 'roman_to_devanagari', 'devanagari_to_roman', or None for auto-detection."

# Example Usage:
# if __name__ == "__main__":
       
#     # Auto-detection example
#     mixed_examples = [
#         "नमस्ते my friend मुझे हिंदी सीखना पसंद है"
#     ]
    
#     print("=== Auto-detection Examples ===")
#     for example in mixed_examples:
#         result = transliterate_text(example)  # Auto-detect direction
#         print(f"Input: {example}")
#         print(f"Output: {result}")
#         print(f"Detected: {detect_script(example)}")
#         print()

