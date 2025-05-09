import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './App';
import Dashboard from './Dashboard';
import Phq9Form from './Phq9Form.tsx';
import BloodPressureForm from './BloodPressureForm.tsx';
import AudioUploadForm from './AudioUploadForm.tsx';
import VideoUploadForm from './VideoUploadForm.tsx';
import HistoryChart from './HistoryChart.tsx';

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/phq9" element={<Phq9Form />} />
        <Route path="/blood-pressure" element={<BloodPressureForm />} />
        <Route path="/audio-upload" element={<AudioUploadForm />} />
        <Route path="/video-upload" element={<VideoUploadForm />} />
        <Route path="/history" element={<HistoryChart />} />
      </Routes>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);
