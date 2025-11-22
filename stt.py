# stt.py
import whisper

# Load the Whisper model once globally (can be moved to a class if needed)
model = whisper.load_model("base")

def audio(file_path):
    """Transcribes speech from the given audio file in Hindi."""
    result = model.transcribe(file_path, language="hi")
    return result["text"]
