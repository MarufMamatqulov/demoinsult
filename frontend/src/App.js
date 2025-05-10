import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './AssessmentForms.css';
import SpeechHearingForm from './SpeechHearingForm';
import MovementForm from './MovementForm';
import BloodPressureForm from './BloodPressureForm';
import Phq9Form from './Phq9Form';
import Dashboard from './Dashboard';
import Navbar from './Navbar';
import Footer from './Footer';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/speech-hearing-assessment" element={<SpeechHearingForm />} />
            <Route path="/movement-assessment" element={<MovementForm />} />
            <Route path="/blood-pressure" element={<BloodPressureForm />} />
            <Route path="/phq9" element={<Phq9Form />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
