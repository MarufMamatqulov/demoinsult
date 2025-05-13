import React, { useState } from 'react';
import axios from 'axios';
import './AIRecommendations.css';

// Component Props Interface
interface AIRecommendationsProps {
  assessmentType: string;
  assessmentData: any;
  language: string;
}

const AIRecommendations: React.FC<AIRecommendationsProps> = ({ assessmentType, assessmentData, language }) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [aiResponse, setAiResponse] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<string[] | null>(null);

  // Function to get analysis from OpenAI
  const getAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:8000/ai/rehabilitation/analysis', {
        assessment_data: assessmentData,
        assessment_type: assessmentType,
        language: language
      });
      
      setAiResponse(response.data.response);
      setRecommendations(response.data.recommendations);
    } catch (err) {
      console.error('Error getting AI recommendations:', err);
      setError('Failed to get AI analysis. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // Function to handle user questions about their assessment
  const askQuestion = async (question: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:8000/ai/chat/completion', {
        messages: [
          { role: 'user', content: question }
        ],
        language: language,
        context: {
          assessment_type: assessmentType,
          assessment_data: assessmentData
        }
      });
      
      setAiResponse(response.data.response);
    } catch (err) {
      console.error('Error asking question:', err);
      setError('Failed to get an answer. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // Get translations based on language
  const getTranslation = (key: string): string => {
    const translations: { [key: string]: { [key: string]: string } } = {
      analyzeButton: {
        en: 'Analyze with AI',
        ru: 'Анализировать с ИИ',
        uz: 'AI bilan tahlil qilish'
      },
      loadingText: {
        en: 'Getting AI analysis...',
        ru: 'Получение анализа ИИ...',
        uz: 'AI tahlilini olish...'
      },
      recommendationsTitle: {
        en: 'AI Recommendations',
        ru: 'Рекомендации ИИ',
        uz: 'AI tavsiyalari'
      },
      analysisTitle: {
        en: 'Analysis',
        ru: 'Анализ',
        uz: 'Tahlil'
      },
      askQuestionPlaceholder: {
        en: 'Ask a question about your assessment...',
        ru: 'Задайте вопрос о вашей оценке...',
        uz: 'Baholashingiz haqida savol bering...'
      },
      askButton: {
        en: 'Ask',
        ru: 'Спросить',
        uz: 'So\'rash'
      }
    };

    return translations[key][language] || translations[key]['en'];
  };

  // Controlled input for questions
  const [question, setQuestion] = useState('');

  return (
    <div className="ai-recommendations-container">
      {!aiResponse && !loading && (
        <button 
          onClick={getAnalysis} 
          className="analyze-button"
          disabled={loading}
        >
          {getTranslation('analyzeButton')}
        </button>
      )}

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>{getTranslation('loadingText')}</p>
        </div>
      )}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {aiResponse && (
        <div className="ai-response">
          <h3>{getTranslation('analysisTitle')}</h3>
          <div className="analysis-text">
            {aiResponse.split('\n').map((line, index) => (
              <p key={index}>{line}</p>
            ))}
          </div>

          {recommendations && recommendations.length > 0 && (
            <div className="recommendations">
              <h3>{getTranslation('recommendationsTitle')}</h3>
              <ul>
                {recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="ask-question">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder={getTranslation('askQuestionPlaceholder')}
              className="question-input"
            />
            <button 
              onClick={() => {
                if (question.trim()) {
                  askQuestion(question);
                  setQuestion('');
                }
              }}
              className="ask-button"
              disabled={loading || !question.trim()}
            >
              {getTranslation('askButton')}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIRecommendations;
