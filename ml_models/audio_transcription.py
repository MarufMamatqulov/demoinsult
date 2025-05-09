import whisper

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribes an audio file to text using OpenAI's Whisper model.

    Args:
        audio_file_path (str): Path to the audio file (mp3/wav).

    Returns:
        str: Transcribed text.
    """
    # Load the Whisper model
    model = whisper.load_model("base")

    # Transcribe the audio file
    result = model.transcribe(audio_file_path)

    # Return the transcribed text
    return result['text']

if __name__ == "__main__":
    # Example usage
    audio_path = "example_audio.mp3"  # Replace with your audio file path
    transcription = transcribe_audio(audio_path)
    print("Transcription:", transcription)
