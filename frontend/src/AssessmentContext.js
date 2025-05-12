import React, { createContext, useState, useContext } from 'react';

const AssessmentContext = createContext(undefined);

export const AssessmentProvider = ({ children }) => {
  const [assessmentData, setAssessmentData] = useState(null);
  
  return (
    <AssessmentContext.Provider value={{ assessmentData, setAssessmentData }}>
      {children}
    </AssessmentContext.Provider>
  );
};

export const useAssessment = () => {
  const context = useContext(AssessmentContext);
  if (context === undefined) {
    throw new Error('useAssessment must be used within an AssessmentProvider');
  }
  return context;
};
