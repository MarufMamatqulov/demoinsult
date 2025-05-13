import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './RehabilitationExercises.css';
// @ts-ignore - Import JSON file
import exercisesData from './data/rehabilitationExercises.json';

const RehabilitationExercises = () => {
  const { i18n } = useTranslation();
  const [activeTab, setActiveTab] = useState('videos');
  const [activeVideo, setActiveVideo] = useState(null);
  
  // Determine the current language for content selection
  const currentLanguage = i18n.language.startsWith('es') ? 'en' : 
                          i18n.language.startsWith('ru') ? 'ru' : 
                          i18n.language.startsWith('uz') ? 'uz' : 'en';
  
  const getTitle = (item) => {
    return currentLanguage === 'ru' ? item.titleRu : 
           currentLanguage === 'uz' ? item.titleUz : 
           item.titleEn;
  };
  
  const getDescription = (item) => {
    return currentLanguage === 'ru' ? item.descriptionRu : 
           currentLanguage === 'uz' ? item.descriptionUz : 
           item.descriptionEn;
  };
  
  const handleVideoClick = (video) => {
    setActiveVideo(video);
    // Scroll to video player
    document.getElementById('video-player')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="rehabilitation-exercises">
      <h2 className="section-title">
        {currentLanguage === 'ru' ? 'Реабилитационные упражнения' : 
         currentLanguage === 'uz' ? 'Reabilitatsiya mashqlari' : 
         'Rehabilitation Exercises'}
      </h2>
      
      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'videos' ? 'active' : ''}`} 
          onClick={() => setActiveTab('videos')}
        >
          {currentLanguage === 'ru' ? 'Видео упражнения' : 
           currentLanguage === 'uz' ? 'Video mashqlar' : 
           'Video Exercises'}
        </button>
        <button 
          className={`tab ${activeTab === 'articles' ? 'active' : ''}`} 
          onClick={() => setActiveTab('articles')}
        >
          {currentLanguage === 'ru' ? 'Полезные статьи' : 
           currentLanguage === 'uz' ? 'Foydali maqolalar' : 
           'Useful Articles'}
        </button>
        <button 
          className={`tab ${activeTab === 'cognitive' ? 'active' : ''}`} 
          onClick={() => setActiveTab('cognitive')}
        >
          {currentLanguage === 'ru' ? 'Память и речь' : 
           currentLanguage === 'uz' ? 'Xotira va nutq' : 
           'Memory & Speech'}
        </button>
      </div>
      
      {activeTab === 'videos' && (
        <div className="content-section videos-section">
          {activeVideo && (
            <div id="video-player" className="video-player-container">
              <h3>{getTitle(activeVideo)}</h3>
              <div className="video-player">
                <iframe
                  src={activeVideo.url}
                  title={getTitle(activeVideo)}
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                ></iframe>
              </div>
              <p className="video-description">{getDescription(activeVideo)}</p>
            </div>
          )}
          
          <div className="video-thumbnails">
            {exercisesData.videoExercises.map((video) => (
              <div 
                key={video.id} 
                className={`video-thumbnail ${activeVideo?.id === video.id ? 'active' : ''}`}
                onClick={() => handleVideoClick(video)}
              >
                <div className="thumbnail-image">                  <img src={video.thumbnail} alt={getTitle(video)} onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = '/images/video-placeholder.jpg';
                  }} />
                  <div className="play-icon">▶</div>
                </div>
                <h4>{getTitle(video)}</h4>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {activeTab === 'articles' && (
        <div className="content-section articles-section">
          <div className="articles-grid">
            {exercisesData.usefulArticles.map((article) => (
              <a 
                key={article.id} 
                href={article.url} 
                className="article-card"
                target="_blank" 
                rel="noopener noreferrer"
              >
                <div className="article-image">                  <img src={article.thumbnail} alt={getTitle(article)} onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = '/images/article-placeholder.jpg';
                  }} />
                </div>
                <h4>{getTitle(article)}</h4>
                <p>{getDescription(article)}</p>
              </a>
            ))}
          </div>
        </div>
      )}
      
      {activeTab === 'cognitive' && (
        <div className="content-section cognitive-section">
          <div className="cognitive-grid">
            {exercisesData.cognitiveExercises.map((exercise) => (
              <a 
                key={exercise.id} 
                href={exercise.url} 
                className="cognitive-card"
                target="_blank" 
                rel="noopener noreferrer"
              >
                <div className="cognitive-image">                  <img src={exercise.thumbnail} alt={getTitle(exercise)} onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = '/images/cognitive-placeholder.jpg';
                  }} />
                </div>
                <h4>{getTitle(exercise)}</h4>
                <p>{getDescription(exercise)}</p>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default RehabilitationExercises;