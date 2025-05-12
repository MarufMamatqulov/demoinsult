import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './Navbar.css';
import './Dropdown.css';

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
      </div>      <ul className={`navbar-links ${isMobileMenuOpen ? 'mobile-visible' : 'mobile-hidden'}`}>
        <li><Link to="/">Home</Link></li>
        <li className="dropdown">
          <span className="dropdown-toggle">Assessments</span>
          <div className="dropdown-menu">
            <Link to="/blood-pressure">Blood Pressure</Link>
            <Link to="/speech-hearing-assessment">Speech & Hearing</Link>
            <Link to="/movement-assessment">Movement</Link>
            <Link to="/phq9">PHQ-9</Link>
            <Link to="/nihss">NIHSS</Link>
          </div>
        </li>        <li><Link to="/rehabilitation">Rehabilitation Analysis</Link></li>
        <li><Link to="/patient-chat" className="highlight-link">AI Assistant</Link></li>
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
