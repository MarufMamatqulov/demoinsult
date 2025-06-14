import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from './context/AuthContext';
import axios from 'axios';
import './FormMedical.css';
import { getPatientInfoLabels, getFormActionText, getLocalizedMessages } from './utils/languageUtils';
import { useAssessment } from './AssessmentContext.js';
import AIRecommendations from './AIRecommendations';

const questions = {
  en: [
    // Speech assessment questions (1-5)
    "1. Can the patient speak clearly with proper pronunciation?",
    "2. Can the patient form complete sentences without struggle?",
    "3. Can the patient maintain normal speech speed and rhythm?",
    "4. Can the patient recall and use appropriate words during conversation?",
    "5. Can the patient's speech be easily understood by strangers?",
    // Hearing assessment questions (6-10)
    "6. Can the patient hear normal conversation without asking for repetition?",
    "7. Can the patient hear sounds from another room (doorbell, phone)?",
    "8. Can the patient distinguish between different voices (male/female)?",
    "9. Can the patient understand speech in noisy environments?",
    "10. Does the patient respond appropriately to questions without misunderstanding?"
  ],
  es: [
    // Spanish translation
    "1. ¿Puede el paciente hablar claramente con pronunciación adecuada?",
    "2. ¿Puede el paciente formar oraciones completas sin dificultad?",
    "3. ¿Puede el paciente mantener una velocidad y ritmo normal del habla?",
    "4. ¿Puede el paciente recordar y usar palabras apropiadas durante la conversación?",
    "5. ¿Puede el habla del paciente ser fácilmente entendida por extraños?",
    "6. ¿Puede el paciente escuchar una conversación normal sin pedir repetición?",
    "7. ¿Puede el paciente escuchar sonidos desde otra habitación (timbre, teléfono)?",
    "8. ¿Puede el paciente distinguir entre diferentes voces (hombre/mujer)?",
    "9. ¿Puede el paciente entender el habla en entornos ruidosos?",
    "10. ¿El paciente responde adecuadamente a las preguntas sin malentendidos?"
  ],
  ru: [
    // Russian translation
    "1. Может ли пациент говорить четко с правильным произношением?",
    "2. Может ли пациент составлять полные предложения без затруднений?",
    "3. Может ли пациент поддерживать нормальную скорость и ритм речи?",
    "4. Может ли пациент вспоминать и использовать подходящие слова во время разговора?",
    "5. Может ли речь пациента быть легко понята незнакомыми людьми?",
    "6. Может ли пациент слышать обычный разговор, не прося повторения?",
    "7. Может ли пациент слышать звуки из другой комнаты (дверной звонок, телефон)?",
    "8. Может ли пациент различать разные голоса (мужской/женский)?",
    "9. Может ли пациент понимать речь в шумной обстановке?",
    "10. Отвечает ли пациент правильно на вопросы без недопонимания?"
  ],
  uz: [
    // Uzbek translation
    "1. Bemor aniq va to'g'ri talaffuz bilan gapira oladimi?",
    "2. Bemor qiynalmasdan to'liq gaplarni shakllantira oladimi?",
    "3. Bemor normal nutq tezligi va ritmini saqlab qola oladimi?",
    "4. Bemor suhbat paytida tegishli so'zlarni eslash va ishlatish qobiliyatiga egami?",
    "5. Bemorning nutqini notanish odamlar osonlikcha tushuna oladimi?",
    "6. Bemor takrorlashni so'ramasdan oddiy suhbatni eshita oladimi?",
    "7. Bemor boshqa xonadan kelayotgan ovozlarni (eshik qo'ng'irog'i, telefon) eshita oladimi?",
    "8. Bemor turli ovozlarni (erkak/ayol) farqlay oladimi?",
    "9. Bemor shovqinli muhitda nutqni tushuna oladimi?",
    "10. Bemor savollarga noto'g'ri tushunmasdan tegishli javob beradimi?"
  ]
};

const scoreDescriptions = {
  en: [
    "0 - Unable to perform",
    "1 - Severe difficulty",
    "2 - Moderate difficulty",
    "3 - No difficulty"
  ],
  es: [
    "0 - No puede realizar",
    "1 - Dificultad severa",
    "2 - Dificultad moderada",
    "3 - Sin dificultad"
  ],
  ru: [
    "0 - Не может выполнить",
    "1 - Серьезные затруднения",
    "2 - Умеренные затруднения",
    "3 - Без затруднений"
  ],
  uz: [
    "0 - Bajara olmaydi",
    "1 - Jiddiy qiyinchilik",
    "2 - O'rtacha qiyinchilik",
    "3 - Qiyinchilik yo'q"
  ]
};

export default function SpeechHearingForm() {
  const { t, i18n } = useTranslation();
  const { token, isAuthenticated } = useAuth();
  const [patientName, setPatientName] = useState('');
  const [patientAge, setPatientAge] = useState('');
  const [relationship, setRelationship] = useState('');
  const [scores, setScores] = useState(Array(10).fill(0));
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const { setAssessmentData: setContextAssessmentData } = useAssessment();
  
  // API URL from environment variable
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Refactored currentLanguage logic
  const currentLanguage = i18n.language.startsWith('es') ? 'es' : (i18n.language.startsWith('ru') ? 'ru' : (i18n.language.startsWith('uz') ? 'uz' : 'en'));

  const handleScoreChange = (index, value) => {
    const newScores = [...scores];
    newScores[index] = parseInt(value);
    setScores(newScores);
  };
  const [assessmentData, setAssessmentData] = useState(null);
  const [exportLoading, setExportLoading] = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult('');
    setAssessmentData(null);

    // Prepare the data
    const questionsData = scores.map((score, index) => ({
      id: index + 1,
      score: score
    }));

    try {
      const response = await fetch('http://localhost:8000/assessment/speech-hearing', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          questions: questionsData,
          language: currentLanguage,
          patient_name: patientName,
          patient_age: parseInt(patientAge),
          assessor_relationship: relationship
        })
      });

      const data = await response.json();
        
      // Save assessment data for PDF export and chat integration
      const assessmentData = {
        ...data,
        patient_name: patientName,
        patient_age: parseInt(patientAge),
        assessmentType: "speech-hearing",
        assessmentResults: {
          speech_score: data.speech_score,
          hearing_score: data.hearing_score,
          total_score: data.total_score,
          speech_level: data.speech_level,
          hearing_level: data.hearing_level,
          overall_level: data.overall_level
        }
      };
      
      setAssessmentData(assessmentData);
      
      // Make the assessment data available to the floating chat
      setContextAssessmentData(assessmentData);
      
      // Format the result
      let formattedResult = '';
      
      if (currentLanguage === 'es') {
        formattedResult = `
          <h3>Resultados:</h3>
          <p><strong>Puntuación del habla:</strong> ${data.speech_score}/15 (${data.speech_level})</p>
          <p><strong>Puntuación de audición:</strong> ${data.hearing_score}/15 (${data.hearing_level})</p>
          <p><strong>Puntuación total:</strong> ${data.total_score}/30 (${data.overall_level})</p>
          <h3>Recomendaciones de IA:</h3>
          <p>${data.recommendations.replace(/\n/g, '<br>')}</p>
        `;
      } else if (currentLanguage === 'ru') {
        formattedResult = `
          <h3>Результаты:</h3>
          <p><strong>Оценка речи:</strong> ${data.speech_score}/15 (${data.speech_level})</p>
          <p><strong>Оценка слуха:</strong> ${data.hearing_score}/15 (${data.hearing_level})</p>
          <p><strong>Общая оценка:</strong> ${data.total_score}/30 (${data.overall_level})</p>
          <h3>Рекомендации ИИ:</h3>
          <p>${data.recommendations.replace(/\n/g, '<br>')}</p>
        `;
      } else if (currentLanguage === 'uz') {
        formattedResult = `
          <h3>Natijalar:</h3>
          <p><strong>Nutq bahosi:</strong> ${data.speech_score}/15 (${data.speech_level})</p>
          <p><strong>Eshitish bahosi:</strong> ${data.hearing_score}/15 (${data.hearing_level})</p>
          <p><strong>Umumiy baho:</strong> ${data.total_score}/30 (${data.overall_level})</p>
          <h3>AI tavsiyalari:</h3>
          <p>${data.recommendations.replace(/\n/g, '<br>')}</p>
        `;
      } else {
        formattedResult = `
          <h3>Results:</h3>
          <p><strong>Speech Score:</strong> ${data.speech_score}/15 (${data.speech_level})</p>
          <p><strong>Hearing Score:</strong> ${data.hearing_score}/15 (${data.hearing_level})</p>
          <p><strong>Total Score:</strong> ${data.total_score}/30 (${data.overall_level})</p>
          <h3>AI Recommendations:</h3>
          <p>${data.recommendations.replace(/\n/g, '<br>')}</p>
        `;
      }
      
      setResult(formattedResult);
      
      // If user is authenticated, save the assessment to their history
      if (isAuthenticated && token) {
        try {
          await axios.post(`${API_URL}/assessments`, {
            type: 'speech_hearing',
            data: {
              speech_score: data.speech_score,
              hearing_score: data.hearing_score,
              total_score: data.total_score,
              speech_level: data.speech_level,
              hearing_level: data.hearing_level,
              overall_level: data.overall_level,
              patient_name: patientName,
              patient_age: parseInt(patientAge),
              recommendations: data.recommendations || ''
            }
          }, { 
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          });
          console.log('Speech-Hearing assessment saved to user history');
        } catch (historyErr) {
          console.error('Failed to save Speech-Hearing assessment to history:', historyErr);
        }
      }
    } catch (err) {
      setResult(t('errors.assessment'));
    }
    
    setLoading(false);
  };

  const getFormTitle = () => {
    if (currentLanguage === 'es') {
      return "Evaluación de Habla y Audición";
    } else if (currentLanguage === 'ru') {
      return "Оценка Речи и Слуха";
    }
    return "Speech and Hearing Assessment";
  };

  const getFormDescription = () => {
    if (currentLanguage === 'es') {
      return "Complete este formulario para evaluar las habilidades de habla y audición del paciente. Esta evaluación debe ser completada por un familiar o cuidador.";
    } else if (currentLanguage === 'ru') {
      return "Заполните эту форму для оценки речевых и слуховых навыков пациента. Эта оценка должна быть заполнена родственником или опекуном.";
    }
    return "Complete this form to assess the patient's speech and hearing abilities. This assessment should be completed by a relative or caregiver.";
  };
  // Using shared language utilities
  const patientInfoLabels = getPatientInfoLabels(currentLanguage);
  const formActionText = getFormActionText(currentLanguage);
    const handleExportPDF = async () => {
    if (!assessmentData) return;
    
    setExportLoading(true);
    
    try {      const response = await fetch('http://localhost:8000/export/assessment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_name: patientName,
          patient_age: parseInt(patientAge),
          assessor_relationship: relationship,
          assessment_type: "speech_hearing",
          assessment_data: assessmentData,
          language: currentLanguage
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Show success message using shared language utilities
        const messages = getLocalizedMessages(currentLanguage);
        alert(messages.pdfSuccess);
      } else {
        throw new Error(data.message || 'Failed to export PDF');
      }
    } catch (err) {
      // Show error message using shared language utilities
      const messages = getLocalizedMessages(currentLanguage);
      alert(messages.pdfError);
    }
    
    setExportLoading(false);
  };

  return (
    <div className="medical-form-container animate-fade-in speech-hearing-form">
      <h2 className="form-title">{getFormTitle()}</h2>
      <p className="form-description">{getFormDescription()}</p>
      
      <form className="medical-form" onSubmit={handleSubmit}>
        <div className="form-group">          <label className="form-label">{patientInfoLabels.patientName}</label>
          <input
            className="form-input"
            type="text"
            value={patientName}
            onChange={(e) => setPatientName(e.target.value)}
            required
          />
        </div>
        
        <div className="form-group">
          <label className="form-label">{patientInfoLabels.patientAge}</label>
          <input
            className="form-input"
            type="number"
            min="1"
            max="120"
            value={patientAge}
            onChange={(e) => setPatientAge(e.target.value)}
            required
          />
        </div>
        
        <div className="form-group">
          <label className="form-label">{patientInfoLabels.relationship}</label>
          <input
            className="form-input"
            type="text"
            value={relationship}
            onChange={(e) => setRelationship(e.target.value)}
            required
          />
        </div>
        
        <h3 className="section-title">
          {currentLanguage === 'es' ? "Evaluación del Habla (Preguntas 1-5)" :
           currentLanguage === 'ru' ? "Оценка Речи (Вопросы 1-5)" :
           "Speech Assessment (Questions 1-5)"}
        </h3>
        
        <div className="score-legend">
          {scoreDescriptions[currentLanguage].map((desc, i) => (
            <div key={i} className="score-description">{desc}</div>
          ))}
        </div>
        
        {questions[currentLanguage].slice(0, 5).map((question, index) => (
          <div className="form-group question-group" key={index}>
            <label className="form-label">{question}</label>
            <div className="score-options">
              {[0, 1, 2, 3].map((score) => (
                <label key={score} className="score-option">
                  <input
                    type="radio"
                    name={`question-${index + 1}`}
                    value={score}
                    checked={scores[index] === score}
                    onChange={() => handleScoreChange(index, score)}
                    required
                  />
                  <span>{score}</span>
                </label>
              ))}
            </div>
          </div>
        ))}
        
        <h3 className="section-title">
          {currentLanguage === 'es' ? "Evaluación de la Audición (Preguntas 6-10)" :
           currentLanguage === 'ru' ? "Оценка Слуха (Вопросы 6-10)" :
           "Hearing Assessment (Questions 6-10)"}
        </h3>
        
        {questions[currentLanguage].slice(5, 10).map((question, index) => (
          <div className="form-group question-group" key={index + 5}>
            <label className="form-label">{question}</label>
            <div className="score-options">
              {[0, 1, 2, 3].map((score) => (
                <label key={score} className="score-option">
                  <input
                    type="radio"
                    name={`question-${index + 6}`}
                    value={score}
                    checked={scores[index + 5] === score}
                    onChange={() => handleScoreChange(index + 5, score)}
                    required
                  />
                  <span>{score}</span>
                </label>
              ))}
            </div>
          </div>
        ))}
        
        <button 
          type="submit" 
          className="submit-button" 
          disabled={loading}
        >          {loading ? formActionText.processing : formActionText.submit}
        </button>
      </form>
        {result && (        <div className="result-container animate-fade-in">
          <div dangerouslySetInnerHTML={{ __html: result }}></div>
          
          {assessmentData && (
            <div className="export-section">
              <button 
                className="export-button"
                onClick={handleExportPDF}
                disabled={exportLoading}
              >                {exportLoading ? formActionText.exporting : formActionText.exportPDF}
              </button>
                {/* Add AI Recommendations component */}
              <AIRecommendations 
                assessmentType="speech" 
                assessmentData={assessmentData} 
                language={localStorage.getItem('i18nextLng')?.split('-')[0] || 'en'}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
