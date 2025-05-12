import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import './PatientChat.css';

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: string;
}

interface PatientChatProps {
  patientContext?: {
    name?: string;
    age?: number;
    assessmentType?: string;
    assessmentResults?: any;
    [key: string]: any;
  };
}

const PatientChat = ({ patientContext = {} as PatientChatProps['patientContext'] }) => {
  const { t, i18n } = useTranslation();
  const [messages, setMessages] = useState([
    {
      role: 'assistant' as const,
      content: t('chat.welcome', 'Hello! I\'m your Stroke Rehab AI assistant. How can I help you today?'),
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [advice, setAdvice] = useState(null as string | null);
  const messagesEndRef = useRef(null as HTMLDivElement | null);
  const inputRef = useRef(null as HTMLTextAreaElement | null);
  
  // Support Uzbek language
  const currentLanguage = i18n.language.startsWith('es') ? 'es' : 
                          i18n.language.startsWith('ru') ? 'ru' : 
                          i18n.language.startsWith('uz') ? 'uz' : 'en';
  
  // When patient context changes (e.g., new assessment results), show an informative message  useEffect(() => {
    if (patientContext?.assessmentType && patientContext?.assessmentResults) {
      // Use assessment type for potential future features
      const systemMessage: Message = {
        role: 'system',      content: t('chat.assessmentLoaded', 'Assessment data loaded. You can ask for personalized advice based on your results.'),
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, systemMessage]);
    }
  }, [patientContext, t]);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    // Focus input when component mounts
    inputRef.current?.focus();
  }, []);
  const handleInputChange = (e: any) => {
    setInput(e.target.value);
  };

  const handleKeyDown = (e: any) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString()
    };

    // Update UI immediately with user message
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);
    setAdvice(null);

    try {
      // Prepare the chat history
      const chatHistory = messages
        .filter(m => m.role !== 'system') // Remove system messages from the history
        .slice(-6) // Keep only the last 6 messages for context
        .concat([userMessage]);      const response = await fetch('http://localhost:8000/chat/patient-chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: chatHistory,
          patient_context: patientContext || {},
          language: currentLanguage,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      // Add the AI response to the messages
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toLocaleTimeString()
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      
      // If there's additional advice, show it
      if (data.advice) {
        setAdvice(data.advice);
      }
      
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage: Message = {
        role: 'assistant',
        content: t('chat.error', 'Sorry, I encountered an error. Please try again later.'),
        timestamp: new Date().toLocaleTimeString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content: t('chat.welcome', 'Hello! I\'m your Stroke Rehab AI assistant. How can I help you today?'),
        timestamp: new Date().toLocaleTimeString()
      }
    ]);
    setAdvice(null);
  };

  const handleAdviceRequest = async () => {
    if (!patientContext || !patientContext.assessmentType || !patientContext.assessmentResults) {
      return; // Can't request advice without assessment context
    }

    setIsTyping(true);
    setAdvice(null);

    try {
      const response = await fetch('http://localhost:8000/chat/assessment-advice', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          assessment_type: patientContext.assessmentType,
          results: patientContext.assessmentResults,
          language: currentLanguage,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      if (data.advice) {
        const assistantMessage: Message = {
          role: 'assistant',
          content: t('chat.adviceIntro', 'Here\'s my detailed advice based on your assessment results:'),
          timestamp: new Date().toLocaleTimeString()
        };
        
        setMessages(prev => [...prev, assistantMessage]);
        setAdvice(data.advice);
      }
      
    } catch (error) {
      console.error('Error getting assessment advice:', error);
      
      // Add error message
      const errorMessage: Message = {
        role: 'assistant',
        content: t('chat.adviceError', 'Sorry, I couldn\'t generate advice right now. Please try again later.'),
        timestamp: new Date().toLocaleTimeString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="patient-chat-container">
      <div className="chat-header">
        <h2>{t('chat.title', 'Stroke Rehabilitation Assistant')}</h2>
        <div className="chat-controls">
          {patientContext && patientContext.assessmentType && (
            <button className="advice-button" onClick={handleAdviceRequest}>
              {t('chat.getAdvice', 'Get Assessment Advice')}
            </button>
          )}
          <button className="clear-button" onClick={handleClearChat}>
            {t('chat.clear', 'Clear Chat')}
          </button>
        </div>
      </div>
      
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}>
            <div className="message-content">
              <p>{message.content}</p>
              <span className="timestamp">{message.timestamp}</span>
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="message assistant-message typing">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {advice && (
        <div className="advice-panel">
          <h3>{t('chat.additionalAdvice', 'Additional Advice')}</h3>
          <div className="advice-content">{advice}</div>
        </div>
      )}

      <div className="chat-input">
        <textarea
          ref={inputRef}
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder={t('chat.placeholder', 'Type your question here...')}
          rows={2}
          disabled={isTyping}
        />
        <button 
          onClick={handleSendMessage} 
          disabled={!input.trim() || isTyping}
          className="send-button"
        >
          {t('chat.send', 'Send')}
        </button>
      </div>

      <div className="chat-footer">
        <p>{t('chat.disclaimer', 'This AI assistant provides general information and is not a replacement for professional medical advice.')}</p>
      </div>
    </div>
  );
};

export default PatientChat;
