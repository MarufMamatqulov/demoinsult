import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './Navbar.css';
import './Dropdown.css';

const Navbar = () => {
  const { i18n } = useTranslation();
  const [isMobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isDropdownOpen, setDropdownOpen] = useState(false);

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!isMobileMenuOpen);
    if (isDropdownOpen) setDropdownOpen(false);
  };
  
  const toggleDropdown = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDropdownOpen(!isDropdownOpen);
  };
  
  // Close mobile menu when clicking a link
  const handleLinkClick = () => {
    setMobileMenuOpen(false);
    setDropdownOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">Stroke AI</div>
      <div className="navbar-hamburger" onClick={toggleMobileMenu}>
        <div></div>
        <div></div>
        <div></div>
      </div>      <ul className={`navbar-links ${isMobileMenuOpen ? 'mobile-visible' : 'mobile-hidden'}`}>
        <li><Link to="/" onClick={handleLinkClick}>Home</Link></li>
        <li className="dropdown">
          <span className="dropdown-toggle" onClick={toggleDropdown}>
            Assessments
            <span className="dropdown-arrow">▼</span>
          </span>
          <div className={`dropdown-menu ${isDropdownOpen ? 'mobile-dropdown-visible' : ''}`}>
            <Link to="/blood-pressure" onClick={handleLinkClick}>Blood Pressure</Link>
            <Link to="/speech-hearing-assessment" onClick={handleLinkClick}>Speech & Hearing</Link>
            <Link to="/movement-assessment" onClick={handleLinkClick}>Movement</Link>
            <Link to="/phq9" onClick={handleLinkClick}>PHQ-9</Link>
            <Link to="/nihss" onClick={handleLinkClick}>NIHSS</Link>
          </div>
        </li>        <li><Link to="/rehabilitation" onClick={handleLinkClick}>Rehabilitation Analysis</Link></li>
        <li><Link to="/patient-chat" onClick={handleLinkClick} className="highlight-link">AI Assistant</Link></li>
        <li><Link to="/about" onClick={handleLinkClick}>About Us</Link></li>
        <li><Link to="/faq" onClick={handleLinkClick}>FAQ</Link></li>
        <li><Link to="/contact" onClick={handleLinkClick}>Contact Us</Link></li>
        <li><Link to="/team" onClick={handleLinkClick}>Our Team</Link></li></ul>
      <div className="navbar-language-selector">
        <button className={i18n.language === 'en' ? 'active' : ''} onClick={() => changeLanguage('en')}>EN</button>
        <button className={i18n.language === 'ru' ? 'active' : ''} onClick={() => changeLanguage('ru')}>RU</button>
        <button className={i18n.language === 'uz' ? 'active' : ''} onClick={() => changeLanguage('uz')}>UZ</button>
      </div>
    </nav>
  );
};

export default Navbar;
