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
  // Add event listeners to improve touch response
  document.addEventListener('touchstart', function() {}, {passive: true});
  
  // Handle double tap zoom prevention on iOS
  document.addEventListener('touchend', function(e) {
    if (e.target.closest('a, button, .clickable')) {
      e.preventDefault();
    }
  }, false);
};

/**
 * Initialize all mobile optimizations
 */
export const initMobileOptimizations = () => {
  detectNotch();
  optimizeTouchEvents();
};
