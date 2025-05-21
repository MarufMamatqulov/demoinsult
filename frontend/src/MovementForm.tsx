import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './FormMedical.css';
import { getPatientInfoLabels, getFormActionText, getLocalizedMessages } from './utils/languageUtils';
import { useAssessment } from './AssessmentContext.js';
import AIRecommendations from './AIRecommendations';

const questions = {
  en: [
    // Upper limb assessment (1-5)
    "1. Can the patient raise their arms above their head?",
    "2. Can the patient hold a cup without trembling?",
    "3. Can the patient button a shirt or blouse?",
    "4. Can the patient pick up small objects (coins, paperclips)?",
    "5. Can the patient write legibly?",
    // Lower limb assessment (6-9)
    "6. Can the patient stand from a sitting position without help?",
    "7. Can the patient walk without assistance?",
    "8. Can the patient walk up and down stairs?",
    "9. Can the patient lift their knees high when walking?",
    // Balance assessment (10-13)
    "10. Can the patient stand on one leg for 5 seconds?",
    "11. Can the patient turn their body around without losing balance?",
    "12. Can the patient walk in a straight line?",
    "13. Can the patient sit down slowly without falling?"
  ],
  es: [
    // Spanish translation
    "1. ¿Puede el paciente levantar los brazos por encima de su cabeza?",
    "2. ¿Puede el paciente sostener una taza sin temblar?",
    "3. ¿Puede el paciente abotonar una camisa o blusa?",
    "4. ¿Puede el paciente recoger objetos pequeños (monedas, clips)?",
    "5. ¿Puede el paciente escribir legiblemente?",
    "6. ¿Puede el paciente levantarse de una posición sentada sin ayuda?",
    "7. ¿Puede el paciente caminar sin asistencia?",
    "8. ¿Puede el paciente subir y bajar escaleras?",
    "9. ¿Puede el paciente levantar las rodillas alto al caminar?",
    "10. ¿Puede el paciente pararse en una pierna durante 5 segundos?",
    "11. ¿Puede el paciente girar su cuerpo sin perder el equilibrio?",
    "12. ¿Puede el paciente caminar en línea recta?",
    "13. ¿Puede el paciente sentarse lentamente sin caerse?"
  ],  ru: [
    // Russian translation
    "1. Может ли пациент поднять руки над головой?",
    "2. Может ли пациент держать чашку без дрожания?",
    "3. Может ли пациент застегнуть рубашку или блузку?",
    "4. Может ли пациент поднять мелкие предметы (монеты, скрепки)?",
    "5. Может ли пациент писать разборчиво?",
    "6. Может ли пациент встать из положения сидя без помощи?",
    "7. Может ли пациент ходить без посторонней помощи?",
    "8. Может ли пациент подниматься и спускаться по лестнице?",
    "9. Может ли пациент высоко поднимать колени при ходьбе?",
    "10. Может ли пациент стоять на одной ноге в течение 5 секунд?",
    "11. Может ли пациент повернуться всем телом, не теряя равновесия?",
    "12. Может ли пациент ходить по прямой линии?",
    "13. Может ли пациент медленно садиться, не падая?"
  ],
  uz: [
    // Uzbek translation
    "1. Bemor qo'llarini boshi ustiga ko'tara oladimi?",
    "2. Bemor qaltiramasdan chashkani ushlab tura oladimi?",
    "3. Bemor ko'ylak yoki bluzka tugmalarini qadash qobiliyatiga egami?",
    "4. Bemor mayda narsalarni (tangalar, qisqichlar) tera oladimi?",
    "5. Bemor tushunarli yoza oladimi?",
    "6. Bemor yordam olmay o'tirgan holatdan tura oladimi?",
    "7. Bemor yordam olmasdan yura oladimi?",
    "8. Bemor zinapoyadan ko'tarilishi va tushishi mumkinmi?",
    "9. Bemor yurganda tizzalarini baland ko'tara oladimi?",
    "10. Bemor bir oyoqda 5 soniya davomida tura oladimi?",
    "11. Bemor muvozanatni yo'qotmasdan tanasini aylantirib tura oladimi?",
    "12. Bemor to'g'ri chiziq bo'ylab yura oladimi?",
    "13. Bemor yiqilmasdan sekin o'tira oladimi?"
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

export default function MovementForm() {
  const { t, i18n } = useTranslation();
  const [patientName, setPatientName] = useState('');
  const [patientAge, setPatientAge] = useState('');
  const [relationship, setRelationship] = useState('');
  const [scores, setScores] = useState(Array(13).fill(0));
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const { setAssessmentData: setContextAssessmentData } = useAssessment();

  const currentLanguage = i18n.language.startsWith('es') ? 'es' : 
                          i18n.language.startsWith('ru') ? 'ru' : 
                          i18n.language.startsWith('uz') ? 'uz' : 'en';

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
      const response = await fetch('http://localhost:8000/assessment/movement', {
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

      const data = await response.json();      // Save assessment data for PDF export and chat integration
      const assessmentData = {
        ...data,
        patient_name: patientName,
        patient_age: parseInt(patientAge),
        assessmentType: "movement",
        assessmentResults: {
          upper_limb_score: data.upper_limb_score,
          lower_limb_score: data.lower_limb_score,
          balance_score: data.balance_score,
          total_score: data.total_score,
          upper_limb_level: data.upper_limb_level,
          lower_limb_level: data.lower_limb_level,
          balance_level: data.balance_level,
          overall_level: data.overall_level
        }
      };
      
      setAssessmentData(assessmentData);
      
      // Make assessment data available for the floating chat through context
      setContextAssessmentData(assessmentData);
      
      // Format the result
      let formattedResult = '';
      
      if (currentLanguage === 'es') {
        formattedResult = `
          <h3>Resultados:</h3>
          <p><strong>Puntuación de extremidades superiores:</strong> ${data.upper_limb_score}/15 (${data.upper_limb_level})</p>
          <p><strong>Puntuación de extremidades inferiores:</strong> ${data.lower_limb_score}/12 (${data.lower_limb_level})</p>
          <p><strong>Puntuación de equilibrio:</strong> ${data.balance_score}/12 (${data.balance_level})</p>
          <p><strong>Puntuación total:</strong> ${data.total_score}/39 (${data.overall_level})</p>
          <h3>Recomendaciones de IA:</h3>
          <p>${data.recommendations.replace(/\n/g, '<br>')}</p>
        `;
      } else if (currentLanguage === 'ru') {
        formattedResult = `
          <h3>Результаты:</h3>
          <p><strong>Оценка верхних конечностей:</strong> ${data.upper_limb_score}/15 (${data.upper_limb_level})</p>
          <p><strong>Оценка нижних конечностей:</strong> ${data.lower_limb_score}/12 (${data.lower_limb_level})</p>
          <p><strong>Оценка равновесия:</strong> ${data.balance_score}/12 (${data.balance_level})</p>
          <p><strong>Общая оценка:</strong> ${data.total_score}/39 (${data.overall_level})</p>
          <h3>Рекомендации ИИ:</h3>
          <p>${data.recommendations.replace(/\n/g, '<br>')}</p>
        `;
      } else if (currentLanguage === 'uz') {
        formattedResult = `
          <h3>Natijalar:</h3>
          <p><strong>Yuqori a'zo bahosi:</strong> ${data.upper_limb_score}/15 (${data.upper_limb_level})</p>
          <p><strong>Quyi a'zo bahosi:</strong> ${data.lower_limb_score}/12 (${data.lower_limb_level})</p>
          <p><strong>Muvozanat bahosi:</strong> ${data.balance_score}/12 (${data.balance_level})</p>
          <p><strong>Umumiy baho:</strong> ${data.total_score}/39 (${data.overall_level})</p>
          <h3>AI tavsiyalari:</h3>
          <p>${data.recommendations.replace(/\n/g, '<br>')}</p>
        `;
      } else {
        formattedResult = `
          <h3>Results:</h3>
          <p><strong>Upper Limb Score:</strong> ${data.upper_limb_score}/15 (${data.upper_limb_level})</p>
          <p><strong>Lower Limb Score:</strong> ${data.lower_limb_score}/12 (${data.lower_limb_level})</p>
          <p><strong>Balance Score:</strong> ${data.balance_score}/12 (${data.balance_level})</p>
          <p><strong>Total Score:</strong> ${data.total_score}/39 (${data.overall_level})</p>
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
      return "Evaluación de Movimiento";
    } else if (currentLanguage === 'ru') {
      return "Оценка Движения";
    }
    return "Movement Assessment";
  };

  const getFormDescription = () => {
    if (currentLanguage === 'es') {
      return "Complete este formulario para evaluar las habilidades de movimiento del paciente. Esta evaluación debe ser completada por un familiar o cuidador.";
    } else if (currentLanguage === 'ru') {
      return "Заполните эту форму для оценки двигательных навыков пациента. Эта оценка должна быть заполнена родственником или опекуном.";
    }
    return "Complete this form to assess the patient's movement abilities. This assessment should be completed by a relative or caregiver.";
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
          assessment_type: "movement",
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
    <div className="medical-form-container animate-fade-in movement-form">
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
          {currentLanguage === 'es' ? "Evaluación de Extremidades Superiores (Preguntas 1-5)" :
           currentLanguage === 'ru' ? "Оценка Верхних Конечностей (Вопросы 1-5)" :
           "Upper Limb Assessment (Questions 1-5)"}
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
          {currentLanguage === 'es' ? "Evaluación de Extremidades Inferiores (Preguntas 6-9)" :
           currentLanguage === 'ru' ? "Оценка Нижних Конечностей (Вопросы 6-9)" :
           "Lower Limb Assessment (Questions 6-9)"}
        </h3>
        
        {questions[currentLanguage].slice(5, 9).map((question, index) => (
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

        <h3 className="section-title">
          {currentLanguage === 'es' ? "Evaluación de Equilibrio (Preguntas 10-13)" :
           currentLanguage === 'ru' ? "Оценка Равновесия (Вопросы 10-13)" :
           "Balance Assessment (Questions 10-13)"}
        </h3>
        
        {questions[currentLanguage].slice(9, 13).map((question, index) => (
          <div className="form-group question-group" key={index + 9}>
            <label className="form-label">{question}</label>
            <div className="score-options">
              {[0, 1, 2, 3].map((score) => (
                <label key={score} className="score-option">
                  <input
                    type="radio"
                    name={`question-${index + 10}`}
                    value={score}
                    checked={scores[index + 9] === score}
                    onChange={() => handleScoreChange(index + 9, score)}
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
        {result && (
        <div className="result-container animate-fade-in">
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
                assessmentType="movement" 
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
