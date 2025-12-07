import os
import shutil
from pathlib import Path
import pypdf
from PIL import Image
import speech_recognition as sr
from pydub import AudioSegment

# Wrap external tools in try-except to prevent app crash if tools are missing
try:
    import pytesseract
    from pdf2image import convert_from_path
except ImportError:
    pytesseract = None
    convert_from_path = None
    print("⚠️ Warning: OCR tools not fully installed. Image/PDF extraction might be limited.")

# Helper to check extensions
ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.mp4', '.mp3', '.wav'}

def process_file(file_path: str, filename: str) -> str:
    """
    Main entry point. Determines file type and extracts text.
    """
    ext = Path(filename).suffix.lower()
    
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
            
    elif ext == ".pdf":
        return extract_pdf(file_path)
        
    elif ext in [".png", ".jpg", ".jpeg"]:
        return extract_image_ocr(file_path)
        
    elif ext in [".mp4", ".mp3", ".wav"]:
        return extract_audio_transcript(file_path)
        
    return ""

def extract_pdf(path):
    text = ""
    try:
        # Try standard text extraction first (fast)
        reader = pypdf.PdfReader(path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        
        # If text is too short, it might be a scanned PDF -> Use OCR
        if len(text) < 50:
            if pytesseract and convert_from_path:
                print("PDF seems scanned. Switching to OCR...")
                images = convert_from_path(path)
                for img in images:
                    text += pytesseract.image_to_string(img) + "\n"
            else:
                return "[Error: OCR tools missing. Cannot read scanned PDF.]"
                
    except Exception as e:
        print(f"PDF Error: {e}")
        return f"[Error reading PDF: {e}]"
        
    return text

def extract_image_ocr(path):
    if not pytesseract:
        return "[Error: pytesseract library not installed]"
    try:
        image = Image.open(path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"[OCR Error: {e}]"

def extract_audio_transcript(path):
    try:
        # 1. Convert to WAV (SpeechRecognition needs WAV)
        audio = AudioSegment.from_file(path)
        
        # Split into 60-second chunks to avoid memory issues/timeouts
        # For this demo, we'll just take the first 2 minutes to keep it fast
        audio = audio[:120000] 
        
        wav_path = path + ".wav"
        audio.export(wav_path, format="wav")
        
        # 2. Transcribe
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            # Uses Google Web Speech API (Free, but rate limited)
            text = recognizer.recognize_google(audio_data)
            
        # Cleanup temp wav
        if os.path.exists(wav_path):
            os.remove(wav_path)
            
        return f"[TRANSCRIPT]: {text}"
        
    except Exception as e:
        print(f"Video/Audio Error: {e}")
        return "[Error: Could not transcribe audio. Ensure ffmpeg is installed.]"