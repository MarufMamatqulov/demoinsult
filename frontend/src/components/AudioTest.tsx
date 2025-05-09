import React, { useState } from 'react';
import axios from 'axios';

const AudioTest = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('/api/audio/analyze', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setResult(response.data);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    return (
        <div className="audio-test">
            <h2>Audio Test</h2>
            <input type="file" accept="audio/*" onChange={handleFileChange} />
            <button onClick={handleUpload}>Start Test</button>

            {result && (
                <div className="result">
                    <h3>Analysis Result</h3>
                    <p><strong>Transcription:</strong> {result.transcription}</p>
                    <p><strong>Speech Clarity:</strong> {result.speech_clarity}%</p>
                    <p><strong>Repetition Score:</strong> {result.repetition_score}</p>
                    <p><strong>Cognitive Risk Level:</strong> {result.cognitive_risk}</p>
                </div>
            )}
        </div>
    );
};

export default AudioTest;
