import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import './styles/Auth.css';

const PasswordResetRequestPage = () => {
  const { requestPasswordReset, error } = useAuth();
  const [email, setEmail] = useState('');
  const [requestSent, setRequestSent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [localError, setLocalError] = useState('');
  
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email) {
      setLocalError('Please enter your email address');
      return;
    }
    
    try {
      setLoading(true);
      setLocalError('');
      await requestPasswordReset(email);
      setRequestSent(true);
    } catch (err) {
      setLocalError((err as Error).message || 'Failed to send password reset request');
    } finally {
      setLoading(false);
    }
  };

  const handleBackToLogin = () => {
    navigate('/login');
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Reset Your Password</h2>
        
        {!requestSent ? (
          <>
            <p className="auth-description">
              Enter your email address and we'll send you a link to reset your password.
            </p>
            
            <form onSubmit={handleSubmit} className="auth-form">
              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  disabled={loading}
                  required
                />
              </div>
              
              {(localError || error) && (
                <div className="auth-error">
                  {localError || error}
                </div>
              )}
              
              <div className="auth-actions">
                <button 
                  type="submit" 
                  className="auth-button"
                  disabled={loading}
                >
                  {loading ? 'Sending...' : 'Send Reset Link'}
                </button>
                
                <button 
                  type="button" 
                  className="auth-button secondary"
                  onClick={handleBackToLogin}
                  disabled={loading}
                >
                  Back to Login
                </button>
              </div>
            </form>
          </>
        ) : (
          <div className="auth-success">
            <div className="success-icon">✓</div>
            <h3>Check Your Email</h3>
            <p>
              We've sent a password reset link to <strong>{email}</strong>. 
              Please check your inbox and follow the instructions to reset your password.
            </p>
            <p className="note">
              If you don't see the email, please check your spam folder.
            </p>
            <button 
              className="auth-button"
              onClick={handleBackToLogin}
            >
              Back to Login
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default PasswordResetRequestPage;
