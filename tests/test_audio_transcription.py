import pytest
from ml_models.audio_transcription import transcribe_audio

def test_transcribe_audio_valid():
    # Replace 'valid_audio.mp3' with the path to a valid audio file for testing
    valid_audio_path = 'valid_audio.mp3'
    result = transcribe_audio(valid_audio_path)
    assert isinstance(result, str) and len(result) > 0, "Expected non-empty transcription"

def test_transcribe_audio_invalid():
    # Replace 'invalid_audio.txt' with the path to an invalid file for testing
    invalid_audio_path = 'invalid_audio.txt'
    with pytest.raises(Exception):
        transcribe_audio(invalid_audio_path)
