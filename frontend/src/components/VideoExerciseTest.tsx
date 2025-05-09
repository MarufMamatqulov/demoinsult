import React, { useState } from 'react';
import axios from 'axios';

const VideoExerciseTest = () => {
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
            const response = await axios.post('/api/video/analyze', formData, {
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
        <div className="video-exercise-test">
            <h2>Video Exercise Test</h2>
            <p>Please do arm raise movement and upload the video.</p>
            <input type="file" accept="video/*" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload Video</button>

            {result && (
                <div className="result">
                    <h3>Analysis Result</h3>
                    <p><strong>Status:</strong> {result.status}</p>
                    <p><strong>Score:</strong> {result.score}/10</p>
                    <p><strong>Feedback:</strong> {result.recommendation}</p>
                </div>
            )}
        </div>
    );
};

export default VideoExerciseTest;
