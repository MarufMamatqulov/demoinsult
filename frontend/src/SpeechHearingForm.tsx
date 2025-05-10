import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './FormMedical.css';

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
  ]
};

export default function SpeechHearingForm() {
  const { t, i18n } = useTranslation();
  const [patientName, setPatientName] = useState('');
  const [patientAge, setPatientAge] = useState('');
  const [relationship, setRelationship] = useState('');
  const [scores, setScores] = useState(Array(10).fill(0));
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const currentLanguage = i18n.language.startsWith('es') ? 'es' : 
                          i18n.language.startsWith('ru') ? 'ru' : 'en';

  const handleScoreChange = (index, value) => {
    const newScores = [...scores];
    newScores[index] = parseInt(value);
    setScores(newScores);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult('');

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

  const getPatientNameLabel = () => {
    if (currentLanguage === 'es') return "Nombre del Paciente";
    if (currentLanguage === 'ru') return "Имя Пациента";
    return "Patient Name";
  };

  const getPatientAgeLabel = () => {
    if (currentLanguage === 'es') return "Edad del Paciente";
    if (currentLanguage === 'ru') return "Возраст Пациента";
    return "Patient Age";
  };

  const getRelationshipLabel = () => {
    if (currentLanguage === 'es') return "Su relación con el paciente";
    if (currentLanguage === 'ru') return "Ваше отношение к пациенту";
    return "Your relationship to patient";
  };

  const getSubmitButtonText = () => {
    if (currentLanguage === 'es') return "Enviar Evaluación";
    if (currentLanguage === 'ru') return "Отправить Оценку";
    return "Submit Assessment";
  };

  return (
    <div className="medical-form-container animate-fade-in speech-hearing-form">
      <h2 className="form-title">{getFormTitle()}</h2>
      <p className="form-description">{getFormDescription()}</p>
      
      <form className="medical-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">{getPatientNameLabel()}</label>
          <input
            className="form-input"
            type="text"
            value={patientName}
            onChange={(e) => setPatientName(e.target.value)}
            required
          />
        </div>
        
        <div className="form-group">
          <label className="form-label">{getPatientAgeLabel()}</label>
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
          <label className="form-label">{getRelationshipLabel()}</label>
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
        >
          {loading ? 
            (currentLanguage === 'es' ? 'Procesando...' : 
             currentLanguage === 'ru' ? 'Обработка...' : 
             'Processing...') : 
            getSubmitButtonText()}
        </button>
      </form>
      
      {result && (
        <div 
          className="result-container animate-fade-in"
          dangerouslySetInnerHTML={{ __html: result }}
        ></div>
      )}
    </div>
  );
}
