import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { useTranslation } from 'react-i18next';
import { GoogleLogin } from '@react-oauth/google';
import './styles/AuthPages.css';

const LoginPage: React.FC = () => {
  const { t } = useTranslation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { login, loginWithGoogle, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  // Redirect if already logged in
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.');
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
      setError(err.message || 'Google login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleGoogleError = () => {
    setError('Google login failed. Please try again or use email login.');
  };
  
  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2>{t('login.title')}</h2>
          <p>{t('login.subtitle')}</p>
        </div>
        
        {error && <div className="auth-error">{error}</div>}
        
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">{t('login.email')}</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={t('login.emailPlaceholder')}
              required
              disabled={isLoading}
            />
          </div>
          
          <div className="form-group password-group">
            <label htmlFor="password">{t('login.password')}</label>
            <div className="password-input-container">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder={t('login.passwordPlaceholder')}
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
          
          <div className="form-options">            <div className="remember-me">
              <input
                type="checkbox"
                id="remember-me"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                disabled={isLoading}
              />
              <label htmlFor="remember-me">{t('login.rememberMe')}</label>
            </div>
            <Link to="/request-password-reset" className="forgot-password-link">
              {t('login.forgotPassword')}
            </Link>
          </div>
          
          <button type="submit" className="primary-button" disabled={isLoading}>
            {isLoading ? t('login.loggingIn') : t('login.loginButton')}
          </button>
        </form>
        
        <div className="auth-divider">
          <span>{t('login.or')}</span>
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
            {t('login.noAccount')} <Link to="/register">{t('login.signUp')}</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
