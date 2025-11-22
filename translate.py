from googletrans import Translator

def translate_maithili_to_english(text):
    translator = Translator()
    result = translator.translate(text, src='auto', dest='en')  # Use 'auto' for language detection
    return result.text
