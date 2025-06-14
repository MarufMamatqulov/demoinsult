import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { useTranslation } from 'react-i18next';
import './styles/ProfilePage.css';

interface ProfileData {
  date_of_birth: string | null;
  gender: string | null;
  height: number | null;
  weight: number | null;
  medical_history: string | null;
  allergies: string | null;
  medications: string | null;
  emergency_contact_name: string | null;
  emergency_contact_phone: string | null;
  doctor_name: string | null;
  doctor_phone: string | null;
  stroke_date: string | null;
  stroke_type: string | null;
  affected_side: string | null;
  mobility_aid: string | null;
  therapy_goals: string | null;
}

const UserProfilePage: React.FC = () => {
  const { t } = useTranslation();
  const { user, getUserProfile, updateProfile, isAuthenticated, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  
  const [activeTab, setActiveTab] = useState('personal');
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
  const [profileFetched, setProfileFetched] = useState(false);
  
  // Profile state
  const [profile, setProfile] = useState<ProfileData>({
    date_of_birth: null,
    gender: null,
    height: null,
    weight: null,
    medical_history: null,
    allergies: null,
    medications: null,
    emergency_contact_name: null,
    emergency_contact_phone: null,
    doctor_name: null,
    doctor_phone: null,
    stroke_date: null,
    stroke_type: null,
    affected_side: null,
    mobility_aid: null,
    therapy_goals: null
  });  // Fetch user profile
  useEffect(() => {
    // Check if user is authenticated first
    if (!isAuthenticated && !authLoading) {
      navigate('/login');
      return;
    }
    
    // Create a reference to track component mount state
    const abortController = new AbortController();
    let isMounted = true;
    
    // Only fetch profile if authenticated, not already loading, and not already fetched
    if (isAuthenticated && !authLoading && !isLoading && !profileFetched) {
      const fetchProfile = async () => {
        try {
          if (!isMounted) return;
          
          setIsLoading(true);
          const profileData = await getUserProfile();
          
          // Only update state if the component is still mounted
          if (isMounted) {
            // Format dates for form inputs
            const formattedProfile = {
              ...profileData,
              date_of_birth: profileData.date_of_birth ? formatDateForInput(profileData.date_of_birth) : null,
              stroke_date: profileData.stroke_date ? formatDateForInput(profileData.stroke_date) : null,
            };
            
            setProfile(formattedProfile);
            setProfileFetched(true);
            setIsLoading(false);
          }
        } catch (error) {
          console.error('Failed to fetch profile:', error);
          if (isMounted) {
            setIsLoading(false);
            setMessage({
              text: t('profile.fetchError'),
              type: 'error'
            });
          }
        }
      };
      
      fetchProfile();
    }
    
    // Cleanup function to prevent state updates if component unmounts
    return () => {
      isMounted = false;
      abortController.abort();
    };
  }, [isAuthenticated, authLoading, getUserProfile, navigate, t, isLoading, profileFetched]);
  
  // Helper function to format date for input
  const formatDateForInput = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toISOString().split('T')[0];
  };
  
  // Handle input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    // Handle number inputs
    if ((type === 'number' || name === 'height' || name === 'weight') && value) {
      setProfile(prev => ({
        ...prev,
        [name]: parseInt(value, 10)
      }));
    } else {
      setProfile(prev => ({
        ...prev,
        [name]: value || null
      }));
    }
  };
    // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      setIsSaving(true);
      await updateProfile(profile);
      setProfileFetched(true); // Mark as fetched since we just updated it
      setMessage({
        text: t('profile.updateSuccess'),
        type: 'success'
      });
      
      // Clear message after 3 seconds
      setTimeout(() => {
        setMessage({ text: '', type: '' });
      }, 3000);
    } catch (error) {
      console.error('Failed to update profile:', error);
      setMessage({
        text: t('profile.updateError'),
        type: 'error'
      });
    } finally {
      setIsSaving(false);
    }
  };
    if (authLoading) {
    return (
      <div className="profile-container loading">
        <div className="loader"></div>
        <p>{t('profile.authenticating')}</p>
      </div>
    );
  }
  
  if (isLoading) {
    return (
      <div className="profile-container loading">
        <div className="loader"></div>
        <p>{t('profile.loading')}</p>
      </div>
    );
  }
  
  if (!isAuthenticated) {
    // Redirect handled in useEffect, but just in case
    navigate('/login');
    return null;
  }
  
  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>{t('profile.title')}</h1>
        <p>{t('profile.subtitle')}</p>
      </div>
      
      {message.text && (
        <div className={`profile-message ${message.type}`}>
          {message.text}
        </div>
      )}
      
      <div className="profile-tabs">
        <button 
          className={`tab-button ${activeTab === 'personal' ? 'active' : ''}`} 
          onClick={() => setActiveTab('personal')}
        >
          {t('profile.tabs.personal')}
        </button>
        <button 
          className={`tab-button ${activeTab === 'medical' ? 'active' : ''}`} 
          onClick={() => setActiveTab('medical')}
        >
          {t('profile.tabs.medical')}
        </button>
        <button 
          className={`tab-button ${activeTab === 'stroke' ? 'active' : ''}`} 
          onClick={() => setActiveTab('stroke')}
        >
          {t('profile.tabs.stroke')}
        </button>
        <button 
          className={`tab-button ${activeTab === 'contacts' ? 'active' : ''}`} 
          onClick={() => setActiveTab('contacts')}
        >
          {t('profile.tabs.contacts')}
        </button>
      </div>
      
      <form onSubmit={handleSubmit} className="profile-form">
        {/* Personal Information Tab */}
        <div className={`tab-content ${activeTab === 'personal' ? 'active' : ''}`}>
          <h2>{t('profile.personalInfo')}</h2>
          
          <div className="form-group">
            <label htmlFor="date_of_birth">{t('profile.dateOfBirth')}</label>
            <input
              type="date"
              id="date_of_birth"
              name="date_of_birth"
              value={profile.date_of_birth || ''}
              onChange={handleChange}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="gender">{t('profile.gender')}</label>
            <select
              id="gender"
              name="gender"
              value={profile.gender || ''}
              onChange={handleChange}
            >
              <option value="">{t('profile.selectGender')}</option>
              <option value="male">{t('profile.male')}</option>
              <option value="female">{t('profile.female')}</option>
              <option value="other">{t('profile.other')}</option>
              <option value="prefer_not_to_say">{t('profile.preferNotToSay')}</option>
            </select>
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="height">{t('profile.height')} (cm)</label>
              <input
                type="number"
                id="height"
                name="height"
                value={profile.height || ''}
                onChange={handleChange}
                min="0"
                max="300"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="weight">{t('profile.weight')} (kg)</label>
              <input
                type="number"
                id="weight"
                name="weight"
                value={profile.weight || ''}
                onChange={handleChange}
                min="0"
                max="500"
              />
            </div>
          </div>
        </div>
        
        {/* Medical Information Tab */}
        <div className={`tab-content ${activeTab === 'medical' ? 'active' : ''}`}>
          <h2>{t('profile.medicalInfo')}</h2>
          
          <div className="form-group">
            <label htmlFor="medical_history">{t('profile.medicalHistory')}</label>
            <textarea
              id="medical_history"
              name="medical_history"
              value={profile.medical_history || ''}
              onChange={handleChange}
              rows={4}
              placeholder={t('profile.medicalHistoryPlaceholder')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="allergies">{t('profile.allergies')}</label>
            <textarea
              id="allergies"
              name="allergies"
              value={profile.allergies || ''}
              onChange={handleChange}
              rows={3}
              placeholder={t('profile.allergiesPlaceholder')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="medications">{t('profile.medications')}</label>
            <textarea
              id="medications"
              name="medications"
              value={profile.medications || ''}
              onChange={handleChange}
              rows={3}
              placeholder={t('profile.medicationsPlaceholder')}
            />
          </div>
        </div>
        
        {/* Stroke Information Tab */}
        <div className={`tab-content ${activeTab === 'stroke' ? 'active' : ''}`}>
          <h2>{t('profile.strokeInfo')}</h2>
          
          <div className="form-group">
            <label htmlFor="stroke_date">{t('profile.strokeDate')}</label>
            <input
              type="date"
              id="stroke_date"
              name="stroke_date"
              value={profile.stroke_date || ''}
              onChange={handleChange}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="stroke_type">{t('profile.strokeType')}</label>
            <select
              id="stroke_type"
              name="stroke_type"
              value={profile.stroke_type || ''}
              onChange={handleChange}
            >
              <option value="">{t('profile.selectStrokeType')}</option>
              <option value="ischemic">{t('profile.ischemicStroke')}</option>
              <option value="hemorrhagic">{t('profile.hemorrhagicStroke')}</option>
              <option value="tia">{t('profile.tia')}</option>
              <option value="other">{t('profile.otherStroke')}</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="affected_side">{t('profile.affectedSide')}</label>
            <select
              id="affected_side"
              name="affected_side"
              value={profile.affected_side || ''}
              onChange={handleChange}
            >
              <option value="">{t('profile.selectAffectedSide')}</option>
              <option value="left">{t('profile.leftSide')}</option>
              <option value="right">{t('profile.rightSide')}</option>
              <option value="both">{t('profile.bothSides')}</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="mobility_aid">{t('profile.mobilityAid')}</label>
            <select
              id="mobility_aid"
              name="mobility_aid"
              value={profile.mobility_aid || ''}
              onChange={handleChange}
            >
              <option value="">{t('profile.selectMobilityAid')}</option>
              <option value="none">{t('profile.noMobilityAid')}</option>
              <option value="cane">{t('profile.cane')}</option>
              <option value="walker">{t('profile.walker')}</option>
              <option value="wheelchair">{t('profile.wheelchair')}</option>
              <option value="other">{t('profile.otherAid')}</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="therapy_goals">{t('profile.therapyGoals')}</label>
            <textarea
              id="therapy_goals"
              name="therapy_goals"
              value={profile.therapy_goals || ''}
              onChange={handleChange}
              rows={4}
              placeholder={t('profile.therapyGoalsPlaceholder')}
            />
          </div>
        </div>
        
        {/* Emergency Contacts Tab */}
        <div className={`tab-content ${activeTab === 'contacts' ? 'active' : ''}`}>
          <h2>{t('profile.emergencyContacts')}</h2>
          
          <div className="form-group">
            <label htmlFor="emergency_contact_name">{t('profile.emergencyContactName')}</label>
            <input
              type="text"
              id="emergency_contact_name"
              name="emergency_contact_name"
              value={profile.emergency_contact_name || ''}
              onChange={handleChange}
              placeholder={t('profile.emergencyContactNamePlaceholder')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="emergency_contact_phone">{t('profile.emergencyContactPhone')}</label>
            <input
              type="tel"
              id="emergency_contact_phone"
              name="emergency_contact_phone"
              value={profile.emergency_contact_phone || ''}
              onChange={handleChange}
              placeholder={t('profile.emergencyContactPhonePlaceholder')}
            />
          </div>
          
          <h2>{t('profile.doctorInfo')}</h2>
          
          <div className="form-group">
            <label htmlFor="doctor_name">{t('profile.doctorName')}</label>
            <input
              type="text"
              id="doctor_name"
              name="doctor_name"
              value={profile.doctor_name || ''}
              onChange={handleChange}
              placeholder={t('profile.doctorNamePlaceholder')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="doctor_phone">{t('profile.doctorPhone')}</label>
            <input
              type="tel"
              id="doctor_phone"
              name="doctor_phone"
              value={profile.doctor_phone || ''}
              onChange={handleChange}
              placeholder={t('profile.doctorPhonePlaceholder')}
            />
          </div>
        </div>
        
        <div className="form-actions">
          <button 
            type="submit" 
            className="save-button" 
            disabled={isSaving}
          >
            {isSaving ? t('profile.saving') : t('profile.saveButton')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default UserProfilePage;
