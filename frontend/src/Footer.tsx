import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './Footer.css';

const Footer = () => {
  const { t } = useTranslation();
  const isMobile = window.innerWidth <= 768;
  
  return (
    <footer className="footer">
      <div className="footer-content">
        {!isMobile && <p dangerouslySetInnerHTML={{ __html: t('footer.copyright') }}></p>}
        {!isMobile && <p>{t('footer.tagline')}</p>}
        <ul className="footer-links">
          <li><Link to="/about">{t('footer.links.about')}</Link></li>
          <li><Link to="/contact">{t('footer.links.contact')}</Link></li>
          <li><Link to="/faq">{t('footer.links.faq')}</Link></li>
        </ul>
        {isMobile && <p className="mobile-copyright">&copy; 2025</p>}
      </div>
    </footer>
  );
};

export default Footer;
