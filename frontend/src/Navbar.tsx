import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './Navbar.css';

const Navbar = () => {
  const { i18n } = useTranslation();
  const [isMobileMenuOpen, setMobileMenuOpen] = useState(false);

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">Stroke AI</div>
      <div className="navbar-hamburger" onClick={toggleMobileMenu}>
        <div></div>
        <div></div>
        <div></div>
      </div>
      <ul className={`navbar-links ${isMobileMenuOpen ? 'mobile-visible' : 'mobile-hidden'}`}>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/rehabilitation">Rehabilitation Analysis</Link></li>
        <li><Link to="/about">About Us</Link></li>
        <li><Link to="/faq">FAQ</Link></li>
        <li><Link to="/contact">Contact Us</Link></li>
        <li><Link to="/team">Our Team</Link></li>
      </ul>
      <div className="navbar-language-selector">
        <button onClick={() => changeLanguage('en')}>EN</button>
        <button onClick={() => changeLanguage('ru')}>RU</button>
        <button onClick={() => changeLanguage('uz')}>UZ</button>
      </div>
    </nav>
  );
};

export default Navbar;
