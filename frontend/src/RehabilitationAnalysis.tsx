import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import RehabilitationExercises from './RehabilitationExercises.tsx';
import './RehabilitationAnalysis.css';

const RehabilitationAnalysis = () => {
  const { i18n } = useTranslation();
  const [activeTab, setActiveTab] = useState('analysis');
  
  // Determine the current language for content selection
  const currentLanguage = i18n.language.startsWith('es') ? 'en' : 
                          i18n.language.startsWith('ru') ? 'ru' : 
                          i18n.language.startsWith('uz') ? 'uz' : 'en';
                          
  const getTitle = () => {
    switch(currentLanguage) {
      case 'ru': return 'Реабилитация после инсульта';
      case 'uz': return 'Insultdan so\'ng reabilitatsiya';
      default: return 'Stroke Rehabilitation';
    }
  };
  
  const getAnalysisTitle = () => {
    switch(currentLanguage) {
      case 'ru': return 'Анализ реабилитации';
      case 'uz': return 'Reabilitatsiya tahlili';
      default: return 'Rehabilitation Analysis';
    }
  };
  
  const getExercisesTitle = () => {
    switch(currentLanguage) {
      case 'ru': return 'Упражнения';
      case 'uz': return 'Mashqlar';
      default: return 'Exercises';
    }
  };
  
  const getDescription = () => {
    switch(currentLanguage) {
      case 'ru': return 'Добро пожаловать на страницу реабилитации после инсульта. Здесь вы можете получить доступ к инструментам и оценкам для реабилитации после инсульта, а также к полезным упражнениям и информационным ресурсам.';
      case 'uz': return 'Insultdan so\'ng reabilitatsiya sahifasiga xush kelibsiz. Bu yerda siz insultdan so\'ng reabilitatsiya uchun vositalar va baholashlar, shuningdek, foydali mashqlar va ma\'lumot resurslariga kirish imkoniyatiga ega bo\'lasiz.';
      default: return 'Welcome to the Stroke Rehabilitation page. Here you can access tools and assessments for stroke rehabilitation, as well as helpful exercises and informational resources.';
    }
  };

  const getAssessmentsList = () => {
    switch(currentLanguage) {
      case 'ru':
        return [
          { name: 'Оценка депрессии PHQ-9', path: '/phq9' },
          { name: 'Шкала инсульта NIHSS', path: '/nihss' },
          { name: 'Мониторинг артериального давления', path: '/blood-pressure' },
          { name: 'Анализ тенденций артериального давления', path: '/bp-trend' },
          { name: 'Оценка разговорной речи', path: '/speech-hearing-assessment' },
          { name: 'Оценка движения', path: '/movement-assessment' },
          { name: 'Анализ аудио', path: '/audio' },
          { name: 'Анализ видео упражнений', path: '/video' }
        ];
      case 'uz':
        return [
          { name: 'PHQ-9 depressiya baholash', path: '/phq9' },
          { name: 'NIHSS insult shkalasi', path: '/nihss' },
          { name: 'Qon bosimi monitoringi', path: '/blood-pressure' },
          { name: 'Qon bosimi trend tahlili', path: '/bp-trend' },
          { name: 'Nutq va eshitish baholash', path: '/speech-hearing-assessment' },
          { name: 'Harakat baholash', path: '/movement-assessment' },
          { name: 'Audio tahlil', path: '/audio' },
          { name: 'Video mashq tahlili', path: '/video' }
        ];
      default:
        return [
          { name: 'PHQ-9 Depression Assessment', path: '/phq9' },
          { name: 'NIHSS Stroke Scale', path: '/nihss' },
          { name: 'Blood Pressure Monitoring', path: '/blood-pressure' },
          { name: 'Blood Pressure Trend Analysis', path: '/bp-trend' },
          { name: 'Speech & Hearing Assessment', path: '/speech-hearing-assessment' },
          { name: 'Movement Assessment', path: '/movement-assessment' },
          { name: 'Audio Analysis', path: '/audio' },
          { name: 'Video Exercise Analysis', path: '/video' }
        ];
    }
  };

  return (
    <div className="rehab-container">
      <h1 className="rehab-title">{getTitle()}</h1>
      <p className="rehab-description">{getDescription()}</p>
      
      <div className="rehab-tabs">
        <button 
          className={`rehab-tab ${activeTab === 'analysis' ? 'active' : ''}`}
          onClick={() => setActiveTab('analysis')}
        >
          {getAnalysisTitle()}
        </button>
        <button 
          className={`rehab-tab ${activeTab === 'exercises' ? 'active' : ''}`}
          onClick={() => setActiveTab('exercises')}
        >
          {getExercisesTitle()}
        </button>
      </div>
      
      <div className="rehab-content">
        {activeTab === 'analysis' ? (
          <div className="analysis-section">
            <div className="assessments-grid">
              {getAssessmentsList().map((assessment, index) => (
                <Link to={assessment.path} key={index} className="assessment-card">
                  <h3>{assessment.name}</h3>
                  <div className="card-arrow">→</div>
                </Link>
              ))}
            </div>
          </div>
        ) : (
          <RehabilitationExercises />
        )}
      </div>
    </div>
  );
};

export default RehabilitationAnalysis;
