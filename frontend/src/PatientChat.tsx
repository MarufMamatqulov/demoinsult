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
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [advice, setAdvice] = useState<string | null>(null);
  let currentLanguage = 'en';

  useEffect(() => {
    if (i18n.language.startsWith('es')) {
      currentLanguage = 'es';
    } else if (i18n.language.startsWith('ru')) {
      currentLanguage = 'ru';
    } else if (i18n.language.startsWith('uz')) {
      currentLanguage = 'uz';
    } else {
      currentLanguage = 'en';
    }
  }, [i18n.language]);

  useEffect(() => {
    if (patientContext?.assessmentType && patientContext?.assessmentResults) {
      const systemMessage: Message = {
        role: 'system',
        content: t('chat.assessmentLoaded', 'Assessment data loaded. You can ask for personalized advice based on your results.'),
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, systemMessage]);
    }
  }, [patientContext, t]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
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

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);
    setAdvice(null);

    try {
      const chatHistory = messages
        .filter(m => m.role !== 'system')
        .slice(-6)
        .concat([userMessage]);

      const response = await fetch('http://localhost:8000/chat/patient-chat', {
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

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="patient-chat">
      <div className="messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <span>{message.content}</span>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <textarea
        ref={inputRef}
        value={input}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        placeholder={t('chat.typeMessage', 'Type your message...')}
      />
      {isTyping && <div className="typing-indicator">{t('chat.typing', 'Typing...')}</div>}
    </div>
  );
};

export default PatientChat;
