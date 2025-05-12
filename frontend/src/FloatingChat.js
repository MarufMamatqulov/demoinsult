import React, { useState } from 'react';
import PatientChat from './PatientChat.js';
import './FloatingChat.css';
import { useTranslation } from 'react-i18next';
import { useAssessment } from './AssessmentContext';

const FloatingChat = ({ assessmentData }) => {
  const [isOpen, setIsOpen] = useState(false);
  const { t } = useTranslation();
  const { assessmentData: contextAssessmentData } = useAssessment();

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="floating-chat-container">
      {isOpen ? (
        <div className="floating-chat-window">
          <div className="floating-chat-header">
            <h3>{t('chat.title')}</h3>
            <button onClick={toggleChat} className="close-button">×</button>
          </div>
          <div className="floating-chat-body">
            <PatientChat 
              patientContext={assessmentData || contextAssessmentData || {}} 
            />
          </div>
        </div>
      ) : (
        <button onClick={toggleChat} className="floating-chat-button">
          <span className="chat-icon">💬</span>
          <span className="chat-text">{t('chat.title')}</span>
        </button>
      )}
    </div>
  );
};

export default FloatingChat;
