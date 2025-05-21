/**
 * Mobile utility functions to enhance mobile experience
 */

/**
 * Detects if the device has a notch (like iPhone X and newer)
 * and adds appropriate classes to the document
 */
export const detectNotch = () => {
  // Check if the device has a notch by checking the safe area inset
  if (CSS.supports('padding-top: env(safe-area-inset-top)')) {
    document.body.classList.add('has-notch');
    
    // Add specific classes for iOS devices
    if (/iPhone|iPad|iPod/.test(navigator.userAgent)) {
      document.body.classList.add('ios-device');
    }
  }
};

/**
 * Improves touch response on mobile devices
 */
export const optimizeTouchEvents = () => {
  // Add event listeners to improve touch response with passive option for better scrolling
  document.addEventListener('touchstart', function() {}, {passive: true});
  
  // Enhanced function to properly handle touch events on interactive elements
  const attachTouchHandlers = () => {
    // Target all interactive elements that should respond to touch
    const touchElements = document.querySelectorAll(
      'a, button, .clickable, input[type="submit"], ' +
      'input[type="button"], input[type="radio"] + label, ' + 
      'input[type="checkbox"] + label, .form-radio, .card, ' +
      '.nav-link, .dropdown-toggle, .tab, select, .exercise-card, ' +
      '.assessment-card, .history-item, .faq-question'
    );
    
    touchElements.forEach(el => {
      // Ensure cursor is pointer for all touchable elements
      el.style.cursor = 'pointer';
      
      // Add proper touch feedback without preventing default behavior
      el.addEventListener('touchstart', function(e) {
        // Only add feedback class if this isn't a scrollable area
        if (!e.target.closest('.scrollable, .scroll-container, .scrollable-content')) {
          this.classList.add('touch-active');
        }
      }, {passive: true});
      
      el.addEventListener('touchend', function() {
        this.classList.remove('touch-active');
        
        // For iOS, add a slight delay to improve tap response
        if (/iPhone|iPad|iPod/.test(navigator.userAgent)) {
          setTimeout(() => {
            // Force a redraw to ensure visual response
            this.style.opacity = '0.99';
            setTimeout(() => {
              this.style.opacity = '';
            }, 10);
          }, 10);
        }
      }, {passive: true});
      
      // Ensure we remove the active state if touch is moved away
      el.addEventListener('touchmove', function() {
        this.classList.remove('touch-active');
      }, {passive: true});
      
      // Also handle cancel events
      el.addEventListener('touchcancel', function() {
        this.classList.remove('touch-active');
      }, {passive: true});
    });
  };
  
  // Execute after DOM is loaded
  if (document.readyState === 'complete') {
    attachTouchHandlers();
  } else {
    window.addEventListener('DOMContentLoaded', attachTouchHandlers);
  }
  
  // Re-attach handlers when DOM changes (for dynamically added elements)
  const observer = new MutationObserver((mutations) => {
    attachTouchHandlers();
  });
  
  // Start observing once DOM is loaded
  if (document.readyState === 'complete') {
    observer.observe(document.body, { childList: true, subtree: true });
  } else {
    window.addEventListener('DOMContentLoaded', () => {
      observer.observe(document.body, { childList: true, subtree: true });
    });
  }
};

/**
 * Initialize all mobile optimizations
 */
export const initMobileOptimizations = () => {
  detectNotch();
  optimizeTouchEvents();
};
