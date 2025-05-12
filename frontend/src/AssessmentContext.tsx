import React, { createContext, useState, useContext } from 'react';

interface AssessmentData {
  assessmentType?: string;
  assessmentResults?: any;
  patient_name?: string;
  patient_age?: number;
  [key: string]: any;
}

interface AssessmentContextType {
  assessmentData: AssessmentData | null;
  setAssessmentData: (data: AssessmentData | null) => void;
}

const AssessmentContext = createContext(undefined as AssessmentContextType | undefined);

export const AssessmentProvider = ({ children }: { children: any }) => {
  const [assessmentData, setAssessmentData] = useState(null as AssessmentData | null);
  
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
