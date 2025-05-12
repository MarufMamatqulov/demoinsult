import React from 'react';
import { useTranslation } from 'react-i18next';
import './LanguageSelector.css';

const LanguageSelector = () => {
  const { i18n } = useTranslation();
  
  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };
  
  return (
    <div className="language-selector">
      <button
        className={`language-button ${i18n.language.startsWith('en') ? 'active' : ''}`}
        onClick={() => changeLanguage('en')}
      >
        EN
      </button>
      <button
        className={`language-button ${i18n.language.startsWith('ru') ? 'active' : ''}`}
        onClick={() => changeLanguage('ru')}
      >
        RU
      </button>
      <button
        className={`language-button ${i18n.language.startsWith('uz') ? 'active' : ''}`}
        onClick={() => changeLanguage('uz')}
      >
        UZ
      </button>
    </div>
  );
};

export default LanguageSelector;
