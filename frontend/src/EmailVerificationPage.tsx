import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import './styles/Auth.css';

const EmailVerificationPage = () => {
  const { verifyEmail } = useAuth();
  const [status, setStatus] = useState('verifying');
  const [message, setMessage] = useState('Verifying your email...');
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const verifyUserEmail = async () => {
      try {
        // Extract token from URL query parameters
        const searchParams = new URLSearchParams(location.search);
        const token = searchParams.get('token');

        if (!token) {
          setStatus('error');
          setMessage('Verification token is missing. Please check your email link.');
          return;
        }

        // Call the API to verify the email
        await verifyEmail(token);
        
        setStatus('success');
        setMessage('Your email has been successfully verified! You can now log in to your account.');
      } catch (error) {
        console.error('Email verification error:', error);
        setStatus('error');
        setMessage('Email verification failed. The token may be invalid or expired.');
      }
    };

    verifyUserEmail();
  }, [location.search, verifyEmail]);

  const handleGoToLogin = () => {
    navigate('/login');
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Email Verification</h2>
        
        {status === 'verifying' && (
          <div className="verification-status verifying">
            <div className="spinner"></div>
            <p>{message}</p>
          </div>
        )}
        
        {status === 'success' && (
          <div className="verification-status success">
            <div className="verification-icon success">✓</div>
            <p>{message}</p>
            <button onClick={handleGoToLogin} className="auth-button">
              Go to Login
            </button>
          </div>
        )}
        
        {status === 'error' && (
          <div className="verification-status error">
            <div className="verification-icon error">✗</div>
            <p>{message}</p>
            <p className="error-message">
              If you continue to experience issues, please contact support.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmailVerificationPage;
