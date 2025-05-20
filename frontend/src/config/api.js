// API configuration for the frontend
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// Export API endpoints
export const endpoints = {
  phqAnalyze: `${API_URL}/phq/analyze`,
  phqHistory: `${API_URL}/phq/history`,
  audioUpload: `${API_URL}/audio/upload`,
  videoUpload: `${API_URL}/video/upload`,
  bpAnalyze: `${API_URL}/bp/analyze`,
  nihssAnalyze: `${API_URL}/nihss/analyze`,
  // Add other endpoints as needed
};

export default API_URL;
