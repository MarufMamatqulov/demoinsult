import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import './PatientChat.css';

const PatientChat = ({ patientContext = {} }) => {
  const { t, i18n } = useTranslation();
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: t('chat.welcome', 'Hello! I\'m your Stroke Rehab AI assistant. How can I help you today?'),
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [advice, setAdvice] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  
  // Support Uzbek language
  const currentLanguage = i18n.language.startsWith('es') ? 'es' : 
                          i18n.language.startsWith('ru') ? 'ru' : 
                          i18n.language.startsWith('uz') ? 'uz' : 'en';
  
  // When patient context changes (e.g., new assessment results), show an informative message
  useEffect(() => {
    if (patientContext?.assessmentType && patientContext?.assessmentResults) {
      // Use assessment type for potential future features
      const systemMessage = {
        role: 'system',
        content: t('chat.assessmentLoaded', 'Assessment data loaded. You can ask for personalized advice based on your results.'),
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, systemMessage]);
    }
  }, [patientContext, t]);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };
  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message to chat
    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);
    
    try {
      // Prepare chat history for API request
      const chatHistory = messages
        .filter(m => m.role !== 'system') // Remove system messages from the history
        .slice(-6) // Keep only the last 6 messages for context
        .concat([userMessage]);
      
      // Call API to get response
      const response = await fetch('http://localhost:8000/chat/patient-chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: chatHistory,
          patient_context: patientContext || {},
          language: currentLanguage
        }),
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      
      // Add AI response to chat
      const aiMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toLocaleTimeString()
      };
      
      setMessages(prev => [...prev, aiMessage]);
      
      // If there's personalized advice, save it
      if (data.advice) {
        setAdvice(data.advice);
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        role: 'assistant',
        content: t('chat.error', 'Sorry, I encountered an error. Please try again later.'),
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="chat-container">
      {/* Assessment context info if available */}
      <div className="assessment-context">
        {patientContext && patientContext.assessmentType && (
          <div className="assessment-info">
            <span className="info-icon">ℹ️</span>
            <span>{t('chat.usingAssessment', 'Using assessment data from')}: {patientContext.assessmentType}</span>
          </div>
        )}
      </div>
      
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message-content">{msg.content}</div>
            <div className="message-timestamp">{msg.timestamp}</div>
          </div>
        ))}
        
        {isTyping && (
          <div className="message assistant typing">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <div className="chat-input">
        <textarea
          ref={inputRef}
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder={t('chat.placeholder', 'Type your message...')}
          rows={2}
        />
        <button 
          className="send-button"
          onClick={handleSend}
          disabled={!input.trim()}
        >
          {t('chat.send', 'Send')}
        </button>
      </div>
      
      {advice && (
        <div className="advice-panel">
          <h4>{t('chat.adviceHeading', 'Personalized Advice')}</h4>
          <p>{advice}</p>
        </div>
      )}
    </div>
  );
};

export default PatientChat;
