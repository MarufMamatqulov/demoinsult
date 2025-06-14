import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { useTranslation } from 'react-i18next';
import { GoogleLogin } from '@react-oauth/google';
import './styles/AuthPages.css';

const RegisterPage: React.FC = () => {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    acceptTerms: false
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { register, loginWithGoogle, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  // Redirect if already logged in
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };
  
  const validateForm = () => {
    // Basic validation
    if (formData.password !== formData.confirmPassword) {
      setError(t('register.passwordsDoNotMatch'));
      return false;
    }
    
    if (formData.password.length < 8) {
      setError(t('register.passwordTooShort'));
      return false;
    }
    
    if (!formData.acceptTerms) {
      setError(t('register.acceptTermsRequired'));
      return false;
    }
    
    return true;
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (!validateForm()) {
      return;
    }
    
    setIsLoading(true);
    
    try {
      await register({
        email: formData.email,
        username: formData.username,
        password: formData.password,
        first_name: formData.firstName,
        last_name: formData.lastName
      });
      
      // After successful registration, redirect to login
      navigate('/login', { 
        state: { 
          message: t('register.registrationSuccessful'),
          email: formData.email
        } 
      });
    } catch (err) {
      setError(err.message || t('register.registrationFailed'));
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleGoogleSuccess = async (credentialResponse: any) => {
    try {
      setIsLoading(true);
      await loginWithGoogle(credentialResponse.credential);
      navigate('/');
    } catch (err) {
      setError(err.message || t('register.googleRegistrationFailed'));
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleGoogleError = () => {
    setError(t('register.googleRegistrationFailed'));
  };
  
  return (
    <div className="auth-container">
      <div className="auth-card register-card">
        <div className="auth-header">
          <h2>{t('register.title')}</h2>
          <p>{t('register.subtitle')}</p>
        </div>
        
        {error && <div className="auth-error">{error}</div>}
        
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="firstName">{t('register.firstName')}</label>
              <input
                type="text"
                id="firstName"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                placeholder={t('register.firstNamePlaceholder')}
                disabled={isLoading}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="lastName">{t('register.lastName')}</label>
              <input
                type="text"
                id="lastName"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                placeholder={t('register.lastNamePlaceholder')}
                disabled={isLoading}
              />
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="email">{t('register.email')}</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder={t('register.emailPlaceholder')}
              required
              disabled={isLoading}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="username">{t('register.username')}</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder={t('register.usernamePlaceholder')}
              required
              disabled={isLoading}
            />
          </div>
          
          <div className="form-group password-group">
            <label htmlFor="password">{t('register.password')}</label>
            <div className="password-input-container">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder={t('register.passwordPlaceholder')}
                required
                disabled={isLoading}
              />
              <button
                type="button"
                className="toggle-password-button"
                onClick={() => setShowPassword(!showPassword)}
                tabIndex={-1}
              >
                {showPassword ? (
                  <span className="password-icon">👁️</span>
                ) : (
                  <span className="password-icon">👁️‍🗨️</span>
                )}
              </button>
            </div>
          </div>
          
          <div className="form-group password-group">
            <label htmlFor="confirmPassword">{t('register.confirmPassword')}</label>
            <div className="password-input-container">
              <input
                type={showPassword ? 'text' : 'password'}
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder={t('register.confirmPasswordPlaceholder')}
                required
                disabled={isLoading}
              />
            </div>
          </div>
          
          <div className="form-check">
            <input
              type="checkbox"
              id="acceptTerms"
              name="acceptTerms"
              checked={formData.acceptTerms}
              onChange={handleChange}
              required
              disabled={isLoading}
            />
            <label htmlFor="acceptTerms">
              {t('register.acceptTerms')} <Link to="/terms">{t('register.termsLink')}</Link> {t('register.and')} <Link to="/privacy">{t('register.privacyLink')}</Link>
            </label>
          </div>
          
          <button type="submit" className="primary-button" disabled={isLoading}>
            {isLoading ? t('register.registering') : t('register.registerButton')}
          </button>
        </form>
        
        <div className="auth-divider">
          <span>{t('register.or')}</span>
        </div>
        
        <div className="social-auth">
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={handleGoogleError}
            useOneTap
          />
        </div>
        
        <div className="auth-footer">
          <p>
            {t('register.alreadyHaveAccount')} <Link to="/login">{t('register.signIn')}</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
