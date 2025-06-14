import React, { createContext, useState, useEffect, useContext, useCallback } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// Create context
const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // API URL from environment variable
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Configure axios with token
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      localStorage.setItem('token', token);
    } else {
      delete axios.defaults.headers.common['Authorization'];
      localStorage.removeItem('token');
    }
  }, [token]);
  // Load user profile on mount or token change
  useEffect(() => {
    const loadUserProfile = async () => {
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const response = await axios.get(`${API_URL}/auth/me`);
        setUser(response.data);
        setError(null);
      } catch (err) {
        console.error('Failed to load user profile:', err);
        setError('Failed to load your profile');
        // If token is invalid, clear it
        if (err.response && (err.response.status === 401 || err.response.status === 403)) {
          setToken(null);
          setUser(null);
        }
      } finally {
        setLoading(false);
      }
    };

    loadUserProfile();
  }, [token, API_URL]);

  // Login with email and password
  const login = async (email, password) => {
    try {
      setLoading(true);
      setError(null);

      const formData = new URLSearchParams();
      formData.append('username', email); // OAuth2 spec uses 'username' field
      formData.append('password', password);

      const response = await axios.post(`${API_URL}/auth/login`, formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      // Set token in state and localStorage
      setToken(response.data.access_token);
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Login failed. Please check your credentials.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Register a new account
  const register = async (userData) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.post(`${API_URL}/auth/register`, userData);
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Registration failed. Please try again.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Login with Google
  const loginWithGoogle = async (googleToken) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.post(`${API_URL}/auth/login/google`, {
        token: googleToken,
      });
      setToken(response.data.access_token);
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Google login failed. Please try again.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Logout
  const logout = () => {
    setToken(null);
    setUser(null);
    navigate('/login');
  };

  // Update user profile
  const updateProfile = async (profileData) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.put(`${API_URL}/auth/me/profile`, profileData);
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to update profile. Please try again.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Update user account information
  const updateUserInfo = async (userData) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.put(`${API_URL}/auth/me`, userData);
      setUser(response.data);
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to update user information. Please try again.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };  // Get user profile
  const getUserProfile = useCallback(async () => {
    try {
      // We'll use a local loading state in the component instead of the global one
      // to prevent potential circular dependencies and re-renders
      setError(null);
      const response = await axios.get(`${API_URL}/auth/me/profile`);
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to get profile. Please try again.';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  }, [API_URL, setError]);

  // Verify email address
  const verifyEmail = async (token) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.post(`${API_URL}/auth/verify-email`, { token });
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Email verification failed. Please try again.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Request password reset
  const requestPasswordReset = async (email) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.post(`${API_URL}/auth/request-password-reset`, { email });
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to request password reset. Please try again.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Reset password with token
  const resetPassword = async (token, newPassword) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.post(`${API_URL}/auth/reset-password`, { 
        token,
        new_password: newPassword 
      });
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Password reset failed. Please try again.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Context value
  const value = {
    user,
    token,
    loading,
    error,
    login,
    register,
    logout,
    loginWithGoogle,
    updateProfile,
    updateUserInfo,
    getUserProfile,
    verifyEmail,
    requestPasswordReset,
    resetPassword,
    isAuthenticated: !!token,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
