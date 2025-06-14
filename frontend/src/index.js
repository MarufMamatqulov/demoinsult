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
import LoginPage from './LoginPage.tsx';
import RegisterPage from './RegisterPage.tsx';
import UserProfilePage from './UserProfilePage.tsx';
import AssessmentHistory from './AssessmentHistory.tsx';
import AssessmentDetails from './AssessmentDetails.tsx';
import RehabilitationAnalysis from './RehabilitationAnalysis.tsx';
import EmailVerificationPage from './EmailVerificationPage.tsx';
import PasswordResetRequestPage from './PasswordResetRequestPage.tsx';
import PasswordResetPage from './PasswordResetPage.tsx';
import RegistrationSuccessPage from './RegistrationSuccessPage.tsx';
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
// Import Auth Context Provider
import { AuthProvider } from './context/AuthContext';
// Import FloatingChat component
import FloatingChat from './FloatingChat.js';
// Import Protected Route component
import ProtectedRoute from './components/ProtectedRoute.tsx';
// Import Google OAuth provider
import { GoogleOAuthProvider } from '@react-oauth/google';

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

// Get Google Client ID from environment variable
const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID || '';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <Router>
        <AuthProvider>
          <AssessmentProvider>
            <Navbar />
            <div className="main-content">
              <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                  {/* Public routes */}
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/register" element={<RegisterPage />} />
                  <Route path="/about" element={<AboutUs />} />
                  <Route path="/faq" element={<FAQ />} />
                  <Route path="/contact" element={<ContactUs />} />
                  <Route path="/team" element={<OurTeam />} />
                  <Route path="/verify-email" element={<EmailVerificationPage />} />
                  <Route path="/request-password-reset" element={<PasswordResetRequestPage />} />
                  <Route path="/reset-password" element={<PasswordResetPage />} />
                  <Route path="/registration-success" element={<RegistrationSuccessPage />} />
                  
                  {/* Protected routes */}
                  <Route element={<ProtectedRoute />}>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/profile" element={<UserProfilePage />} />
                    <Route path="/assessment-history" element={<AssessmentHistory />} />
                    <Route path="/assessment-details/:id" element={<AssessmentDetails />} />
                    <Route path="/nihss" element={<NihssForm />} />
                    <Route path="/phq9" element={<Phq9Form />} />
                    <Route path="/bp-trend" element={<BPTrendForm />} />
                    <Route path="/blood-pressure" element={<BloodPressureForm />} />
                    <Route path="/audio" element={<AudioUploadForm />} />
                    <Route path="/video" element={<VideoUploadForm />} />
                    <Route path="/history" element={<HistoryChart />} />
                    <Route path="/rehabilitation" element={<RehabilitationAnalysis />} />
                    <Route path="/speech-hearing-assessment" element={<SpeechHearingForm />} />
                    <Route path="/movement-assessment" element={<MovementForm />} />
                    <Route path="/patient-chat" element={<PatientChat patientContext={{}} />} />
                  </Route>
                </Routes>
              </Suspense>
            </div>
            {/* Add floating chat component that appears on all pages */}
            <FloatingChat />
            <Footer />
          </AssessmentProvider>
        </AuthProvider>
      </Router>
    </GoogleOAuthProvider>
  </React.StrictMode>
);
