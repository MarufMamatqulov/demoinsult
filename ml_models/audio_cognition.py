import whisper
import numpy as np

def analyze_audio(file_path):
    """
    Transcribe and analyze audio for cognitive patterns.

    Args:
        file_path (str): Path to the audio file (.wav or .mp3).

    Returns:
        dict: Structured result with transcription, speech clarity, repetition score, and cognitive risk level.
    """
    # Load Whisper model
    model = whisper.load_model("base")

    # Transcribe audio
    result = model.transcribe(file_path)
    transcription = result['text']

    # Analyze key patterns
    words = transcription.split()
    word_count = len(words)

    # Speech clarity: percentage of unique words
    unique_words = set(words)
    speech_clarity = len(unique_words) / word_count * 100 if word_count > 0 else 0

    # Repetition score: count of repeated words
    repetition_score = word_count - len(unique_words)

    # Cognitive risk level: heuristic based on clarity and repetition
    if speech_clarity < 50 or repetition_score > 10:
        cognitive_risk = "High"
    elif speech_clarity < 70 or repetition_score > 5:
        cognitive_risk = "Moderate"
    else:
        cognitive_risk = "Low"

    return {
        "transcription": transcription,
        "speech_clarity": speech_clarity,
        "repetition_score": repetition_score,
        "cognitive_risk": cognitive_risk
    }
