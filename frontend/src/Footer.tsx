import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './Footer.css';

const Footer = () => {
  const { t } = useTranslation();
  
  return (
    <footer className="footer">
      <div className="footer-content">
        <p dangerouslySetInnerHTML={{ __html: t('footer.copyright') }}></p>
        <p>{t('footer.tagline')}</p>
        <ul className="footer-links">
          <li><Link to="/about">{t('footer.links.about')}</Link></li>
          <li><Link to="/contact">{t('footer.links.contact')}</Link></li>
          <li><Link to="/faq">{t('footer.links.faq')}</Link></li>
        </ul>
      </div>
    </footer>
  );
};

export default Footer;
