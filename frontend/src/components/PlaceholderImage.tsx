import React from 'react';

interface PlaceholderImageProps {
  type: 'video' | 'article' | 'cognitive' | 'general';
  alt: string;
  className?: string;
}

const PlaceholderImage: React.FC<PlaceholderImageProps> = ({ type, alt, className = '' }) => {
  // Determine which placeholder image to show based on type
  const getPlaceholderSrc = () => {
    switch (type) {
      case 'video':
        return '/images/video-placeholder.jpg';
      case 'article':
        return '/images/article-placeholder.jpg';
      case 'cognitive':
        return '/images/cognitive-placeholder.jpg';
      default:
        return '/images/placeholder.jpg';
    }
  };

  return (
    <img 
      src={getPlaceholderSrc()} 
      alt={alt || 'Placeholder image'} 
      className={`placeholder-image ${className}`}
    />
  );
};

export default PlaceholderImage;
