import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './styles/RegistrationSuccess.css';

const RegistrationSuccessPage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const email = location.state?.email || '';
  
  const handleGoToLogin = () => {
    navigate('/login');
  };
  
  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="success-card">
          <div className="success-icon">✓</div>
          <h2>{t('register.registrationSuccessful')}</h2>
          
          <div className="success-message">
            <p>{t('register.verificationEmailSent')}</p>
            <p className="email-sent-to">
              {t('register.emailSentTo')} <strong>{email}</strong>
            </p>
            <p className="verification-instructions">
              {t('register.checkInboxAndSpam')}
            </p>
          </div>
          
          <button 
            className="primary-button"
            onClick={handleGoToLogin}
          >
            {t('register.goToLogin')}
          </button>
          
          <div className="registration-help">
            <p>{t('register.didntReceiveEmail')} <a href="/request-password-reset">{t('register.requestNewVerification')}</a></p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegistrationSuccessPage;
