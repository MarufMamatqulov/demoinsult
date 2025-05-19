import React, { useState } from 'react';
import PatientChat from './PatientChat.js';
import './FloatingChat.css';
import { useTranslation } from 'react-i18next';
import { useAssessment } from './AssessmentContext';

const FloatingChat = ({ assessmentData }) => {
  const [isOpen, setIsOpen] = useState(false);
  const { t } = useTranslation();
  const { assessmentData: contextAssessmentData } = useAssessment();

  const toggleChat = (e) => {
    // Prevent event bubbling to ensure the click is captured
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    
    setIsOpen(!isOpen);
    // Focus the chat input when opened
    if (!isOpen) {
      setTimeout(() => {
        const inputElement = document.querySelector('.floating-chat-body textarea');
        if (inputElement) {
          inputElement.focus();
        }
      }, 100);
    }
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
      ) : (        <button onClick={toggleChat} className="floating-chat-button">
          <span className="chat-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM20 16H6L4 18V4H20V16Z" fill="white"/>
            </svg>
          </span>
          <span className="chat-text">{t('chat.title')}</span>
        </button>
      )}
    </div>
  );
};

export default FloatingChat;
