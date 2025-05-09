import React, { useState } from 'react';
import './FormMedical.css';

const VideoUploadForm = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState('');
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;
        setLoading(true);
        setResult('');
        const formData = new FormData();
        formData.append('file', file);
        try {
            const response = await fetch('/api/video-upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            setResult(data.result);
        } catch (err) {
            setResult('Error uploading video.');
        }
        setLoading(false);
    };

    return (
        <div className="medical-form-container animate-fade-in">
            <h2 className="form-title">Video Upload</h2>
            <form className="medical-form" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label className="form-label">Select Video File</label>
                    <input
                        className="form-input"
                        type="file"
                        accept="video/*"
                        onChange={handleFileChange}
                        required
                    />
                </div>
                <button className="form-submit-btn" type="submit" disabled={loading || !file}>
                    {loading ? 'Uploading...' : 'Upload'}
                </button>
            </form>
            {result && (
                <div className="form-result animate-pop-in">
                    <h3>Result</h3>
                    <p>{result}</p>
                </div>
            )}
        </div>
    );
};

export default VideoUploadForm;
