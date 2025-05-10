// Entry point for the React app
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Dashboard from './Dashboard';
import NihssForm from './NihssForm.tsx';
import Phq9Form from './Phq9Form.tsx';
import BPTrendForm from './BPTrendForm.js';
import BloodPressureForm from './BloodPressureForm.tsx';
import AudioUploadForm from './AudioUploadForm.tsx';
import VideoUploadForm from './VideoUploadForm.tsx';
import HistoryChart from './HistoryChart.tsx';
import AboutUs from './AboutUs.tsx';
import FAQ from './FAQ.tsx';
import ContactUs from './ContactUs.tsx';
import OurTeam from './OurTeam.tsx';
import RehabilitationAnalysis from './RehabilitationAnalysis.tsx';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './i18n';
import { useTranslation } from 'react-i18next';
import Navbar from './Navbar.tsx';
import Footer from './Footer.tsx';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/nihss" element={<NihssForm />} />
        <Route path="/phq9" element={<Phq9Form />} />
        <Route path="/bp-trend" element={<BPTrendForm />} />
        <Route path="/blood-pressure" element={<BloodPressureForm />} />
        <Route path="/audio" element={<AudioUploadForm />} />
        <Route path="/video" element={<VideoUploadForm />} />
        <Route path="/history" element={<HistoryChart />} />
        <Route path="/about" element={<AboutUs />} />
        <Route path="/faq" element={<FAQ />} />
        <Route path="/contact" element={<ContactUs />} />
        <Route path="/team" element={<OurTeam />} />
        <Route path="/rehabilitation" element={<RehabilitationAnalysis />} />
      </Routes>
      <Footer />
    </Router>
  </React.StrictMode>
);
