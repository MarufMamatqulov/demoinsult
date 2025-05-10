import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>&copy; 2025 Stroke Rehabilitation AI Platform. All rights reserved.</p>
        <p>Empowering recovery with advanced AI tools.</p>
        <ul className="footer-links">
          <li><a href="/about">About Us</a></li>
          <li><a href="/contact">Contact Us</a></li>
          <li><a href="/faq">FAQ</a></li>
        </ul>
      </div>
    </footer>
  );
};

export default Footer;
