import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './Dashboard.css';

const Dashboard = () => {
  const { t } = useTranslation();

  return (
    <div className="dashboard-container">
      <h1>{t('dashboard.title')}</h1>
      <div className="dashboard-links">
        <Link to="/phq9">{t('dashboard.phq9')}</Link>
        <Link to="/nihss">{t('dashboard.nihss')}</Link>
        <Link to="/blood-pressure">{t('dashboard.bloodPressure')}</Link>
        <Link to="/bp-trend">{t('dashboard.bpTrend')}</Link>
        <Link to="/audio">{t('dashboard.audio')}</Link>
        <Link to="/video">{t('dashboard.video')}</Link>
        <Link to="/history">{t('dashboard.history')}</Link>
      </div>
    </div>
  );
};

export default Dashboard;
