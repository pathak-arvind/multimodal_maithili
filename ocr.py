import os
import cv2
import numpy as np
from PIL import Image
import pytesseract

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

def preprocess_image(image_filename):
    # Full path to the image
    image_path = image_filename if os.path.isabs(image_filename) else os.path.join(script_dir, image_filename)

    
    # Read image
    image = cv2.imread(image_path)

    if image is None:
        print(f"⚠️ Could not load image: {image_path}")
        return None

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarization using Otsu's threshold
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Noise removal
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # Save preprocessed image
    processed_path = os.path.join(script_dir, image_filename.replace('.png', '_processed.png'))
    cv2.imwrite(processed_path, cleaned)
    
    return processed_path

def extract_text_from_image(image_filename):
    processed_path = preprocess_image(image_filename)

    if processed_path is None:
        return

    # OCR
    text = pytesseract.image_to_string(Image.open(processed_path), lang='hin')

    # Clean output
    cleaned_text = '\n'.join([line.strip() for line in text.strip().split('\n') if line.strip()])
    print("\n--- Extracted Maithili Text ---\n")
    print(cleaned_text)
    return cleaned_text
