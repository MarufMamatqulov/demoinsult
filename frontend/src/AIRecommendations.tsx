import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AIRecommendations.css';

// Component Props Interface
interface AIRecommendationsProps {
  assessmentType: string;
  assessmentData: any;
  language: string;
}

const AIRecommendations: React.FC<AIRecommendationsProps> = ({ assessmentType, assessmentData, language }) => {
  // State declarations first
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [aiResponse, setAiResponse] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<string[] | null>(null);
  const [fallbackAnalysis, setFallbackAnalysis] = useState('');
  const [question, setQuestion] = useState('');
  
  // Function to get analysis - defined BEFORE useEffect
  const getAnalysis = () => {
    setLoading(true);
    setError(null);
    
    // Generate fallback analysis based on assessment type
    let localFallbackAnalysis = '';
    if (assessmentType === "blood_pressure") {
      const systolic = assessmentData?.systolic || 0;
      const diastolic = assessmentData?.diastolic || 0;
      if (systolic > 0 && diastolic > 0) {
        if (systolic >= 140 || diastolic >= 90) {
          localFallbackAnalysis = "Your blood pressure readings suggest hypertension. Consider lifestyle changes and consulting with a healthcare provider.";
        } else if (systolic >= 130 || diastolic >= 80) {
          localFallbackAnalysis = "Your blood pressure is slightly elevated. Regular monitoring and healthy habits are recommended.";
        } else {
          localFallbackAnalysis = "Your blood pressure appears to be in the normal range. Continue maintaining a healthy lifestyle.";
        }
      }
    } else if (assessmentType === "phq9") {
      // Calculate total score for PHQ-9
      const total = Object.values(assessmentData || {}).reduce((sum: number, val: any) => sum + (Number(val) || 0), 0);
      if (total >= 15) {
        localFallbackAnalysis = "Your responses indicate moderately severe to severe depression symptoms. Please consider seeking professional help.";
      } else if (total >= 10) {
        localFallbackAnalysis = "Your responses indicate moderate depression symptoms. Consulting with a healthcare provider is recommended.";
      } else if (total >= 5) {
        localFallbackAnalysis = "Your responses indicate mild depression symptoms. Monitoring your symptoms and discussing with a healthcare provider may be beneficial.";
      } else {
        localFallbackAnalysis = "Your responses indicate minimal or no depression symptoms. Maintaining mental wellness activities is recommended.";
      }
    } else if (assessmentType === "nihss") {
      const total = Object.values(assessmentData || {}).reduce((sum: number, val: any) => sum + (Number(val) || 0), 0);
      if (total >= 16) {
        localFallbackAnalysis = "Your NIHSS score suggests a severe stroke. Immediate medical attention and intensive rehabilitation may be required.";
      } else if (total >= 5) {
        localFallbackAnalysis = "Your NIHSS score suggests a moderate stroke. A comprehensive rehabilitation program is recommended.";
      } else {
        localFallbackAnalysis = "Your NIHSS score suggests a mild stroke. Early rehabilitation intervention can improve recovery outcomes.";
      }
    }
    
    setFallbackAnalysis(localFallbackAnalysis);
    
    // Make API request
    axios.post('http://localhost:8000/ai/rehabilitation/analysis', {
      assessment_data: assessmentData,
      assessment_type: assessmentType,
      language: language
    }, {
      timeout: 30000 // 30 seconds timeout
    })
    .then(response => {
      if (response.data && response.data.response) {
        setAiResponse(response.data.response);
        setRecommendations(response.data.recommendations || null);
      } else {
        // Use fallback if response doesn't contain expected data
        throw new Error("Invalid response format from AI service");
      }
    })
    .catch(err => {
      console.error('Error getting AI recommendations:', err);
      
      // Use fallback analysis if available
      if (localFallbackAnalysis !== '') {
        setAiResponse(localFallbackAnalysis);
        setError("AI service unavailable. Showing basic analysis instead.");
      } else {
        setError('Failed to get AI analysis. Please try again later.');
        // Provide a generic fallback
        setAiResponse("Unable to provide detailed analysis. Please consult with your healthcare provider for a proper assessment of your condition.");
      }
    })
    .finally(() => {
      setLoading(false);
    });
  };

  // Auto-analyze on component mount if assessment data is available
  useEffect(() => {
    if (assessmentType && assessmentData && Object.keys(assessmentData || {}).length > 0) {
      // Add a small delay to make sure other components are mounted
      const timer = setTimeout(() => {
        getAnalysis();
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [assessmentType, assessmentData, language]);

  // Function to handle user questions about their assessment
  const askQuestion = (questionText: string) => {
    setLoading(true);
    setError(null);
    
    axios.post('http://localhost:8000/ai/chat/completion', {
      messages: [
        { role: 'user', content: questionText }
      ],
      language: language,
      context: {
        assessment_type: assessmentType,
        assessment_data: assessmentData
      }
    })
    .then(response => {
      setAiResponse(response.data.response);
    })
    .catch(err => {
      console.error('Error asking question:', err);
      setError('Failed to get an answer. Please try again later.');
    })
    .finally(() => {
      setLoading(false);
    });
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
      errorRetry: {
        en: 'Error connecting to AI service. Click to retry.',
        ru: 'Ошибка подключения к сервису ИИ. Нажмите, чтобы повторить попытку.',
        uz: 'AI xizmatiga ulanishda xatolik. Qayta urinish uchun bosing.'
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
        <div className="error-message" onClick={getAnalysis}>
          {getTranslation('errorRetry')}
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