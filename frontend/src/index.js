// Entry point for the React app
import React, { Suspense } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import './MobileStyles.css'; // Add mobile-specific styles
import { initMobileOptimizations } from './utils/mobileUtils';
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
import Navbar from './Navbar.tsx';
import Footer from './Footer.tsx';
// Import the components that were only in App.js
import MovementForm from './MovementForm.tsx';
import SpeechHearingForm from './SpeechHearingForm.tsx';
import PatientChat from './PatientChat.js';
// Import Assessment Context Provider
import { AssessmentProvider } from './AssessmentContext.js';
// Import FloatingChat component
import FloatingChat from './FloatingChat.js';

// Initialize mobile optimizations
document.addEventListener('DOMContentLoaded', () => {
  initMobileOptimizations();
  
  // Enable mobile interaction testing in development mode
  if (process.env.NODE_ENV === 'development') {
    import('./utils/mobileTest').then(module => {
      // Optional: Enable mobile test button for interactive testing
      module.initMobileInteractionTesting();
      
      // Uncomment the line below to enable touch event logging for debugging
      // module.enableTouchEventLogging();
    });
  }
});

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(  <React.StrictMode>
    <AssessmentProvider>
      <Router>
        <Navbar />
        <div className="main-content">
          <Suspense fallback={<div>Loading...</div>}>
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
              <Route path="/speech-hearing-assessment" element={<SpeechHearingForm />} />              <Route path="/movement-assessment" element={<MovementForm />} />
              <Route path="/patient-chat" element={<PatientChat patientContext={{}} />} />
            </Routes>
          </Suspense>      </div>
      {/* Add floating chat component that appears on all pages */}
      <FloatingChat />
      <Footer />
      </Router></AssessmentProvider>
  </React.StrictMode>
);
