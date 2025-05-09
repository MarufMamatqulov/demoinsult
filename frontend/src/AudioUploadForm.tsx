import React, { useState } from 'react';
import './FormMedical.css';

const AudioUploadForm = () => {
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
      const response = await fetch('/api/audio-upload', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      setResult(data.result);
    } catch (err) {
      setResult('Error uploading audio.');
    }
    setLoading(false);
  };

  return (
    <div className="medical-form-container animate-fade-in">
      <h2 className="form-title">Audio Transcription</h2>
      <form onSubmit={handleSubmit} className="medical-form space-y-4">
        <div className="form-group">
          <label className="form-label" htmlFor="audioFile">Upload Audio File:</label>
          <input
            type="file"
            id="audioFile"
            accept="audio/*"
            onChange={handleFileChange}
            className="form-input border border-gray-300 rounded-md p-2"
            required
          />
        </div>
        <button
          type="submit"
          className="form-submit-btn w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
          disabled={loading || !file}
        >
          {loading ? 'Uploading...' : 'Analyze Audio'}
        </button>
      </form>
      {result && (
        <div className="form-result mt-4 p-4 bg-green-100 text-green-800 rounded-md animate-pop-in">
          Transcription: {result}
        </div>
      )}
    </div>
  );
};

export default AudioUploadForm;
