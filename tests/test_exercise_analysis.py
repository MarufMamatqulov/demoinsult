import pytest
from ml_models.exercise_analysis import analyze_exercise_video

def test_analyze_exercise_video_valid():
    # Replace 'valid_video.mp4' with the path to a valid video file for testing
    valid_video_path = 'valid_video.mp4'
    result = analyze_exercise_video(valid_video_path)
    assert result in ["Correct", "Incorrect"], "Expected 'Correct' or 'Incorrect'"

def test_analyze_exercise_video_invalid():
    # Replace 'invalid_video.txt' with the path to an invalid file for testing
    invalid_video_path = 'invalid_video.txt'
    with pytest.raises(Exception):
        analyze_exercise_video(invalid_video_path)
