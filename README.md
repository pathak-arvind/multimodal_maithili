# Multimodal Maithili NLP System (Demo Version)

This repository contains a demo version of my **Multimodal Maithili NLP Toolkit**, built for low-resource Maithili language processing.  
The system supports **text**, **speech**, and **image** input, performing spell correction, dictionary lookup, preprocessing, and Maithili → English translation.

**Note:**  
This is a *demo release*. Only small sample corpora (5 examples each), one sample audio, and one sample image are included for testing.  
The full corpora and models are not public due to size and licensing.

---

## 🚀 Features

### 1. Text Processing
- Maithili dictionary lookup  
- Spell correction using Trie + edit distance  
- Suffix-based stemming  
- Basic POS-informed processing  
- Sentence reconstruction  
- Maithili → English translation  
- Tkinter-based interactive UI  

### 2. Code-Mixed Maithili–English Processing
- Basic token-level language detection  
- Simple code-mix segmentation  
- Demo corpus with 5 sample entries  

**Note:** Full accuracy requires larger corpora (not included).

### 3. Speech Input (Audio)
- Whisper-based speech-to-text  
- One demo audio file included  
- Supports user audio uploads  

### 4. Image Input (OCR)
- Tesseract OCR integration  
- One demo image included  

---

## 📂 Project Structure

```
multimodal_maithili/
│
├── ui.py                  # Main Tkinter interface
├── translate.py           # Translation functions
├── preprocess.py          # Spell correction, stemming, lookup
├── codemix.py             # Code-mixed text processing
├── transliteration.py     # Roman <-> Devanagari transliteration
│
├── data/
│   ├── corpus/            # Sample corpora (5 examples each)
│   ├── audio_samples/     # 1 demo audio file
│   └── images/            # 1 demo image file
│
└── README.md
```

---

## ▶️ How to Run

### 1. Activate your virtual environment
```
source myenv/bin/activate
```

### 2. Install dependencies
(If using requirements.txt)
```
pip install -r requirements.txt
```

### 3. Launch the UI
```
python ui.py
```

---

## ⚠️ About Missing Full Corpora

Some modules require larger private datasets:

- Full code-mixed Maithili–English corpus  
- Large Maithili lexicon  
- Whisper/STT models  
- OCR training data  

These are not included publicly.  
This repo contains sample files sufficient for demonstration and evaluation.

---

## 👤 Author

**Arvind Pathak**  
B.Tech CSE, IIIT Manipur  
Research Focus: Computational Linguistics & Low-Resource NLP

---


## 📌 Notes

This repository is for demonstration and evaluation only. No license is provided; all rights are reserved. Please do not reuse or distribute the code.

- This is a **demo** version of the full system.  
- Core pipeline and UI are included.  
- Larger models/corpora can be integrated privately.  
