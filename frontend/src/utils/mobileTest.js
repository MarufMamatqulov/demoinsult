/**
 * Mobile interaction testing utilities
 * Use this file to test mobile interactions on real devices
 */

/**
 * Logs mobile touch events to help with debugging
 * Add the following to your app for testing:
 * import { enableTouchEventLogging } from './utils/mobileTest';
 * enableTouchEventLogging();
 */
export const enableTouchEventLogging = () => {
  // Create a floating log display
  const createLogDisplay = () => {
    const logContainer = document.createElement('div');
    logContainer.style.position = 'fixed';
    logContainer.style.bottom = '10px';
    logContainer.style.left = '10px';
    logContainer.style.zIndex = '9999';
    logContainer.style.backgroundColor = 'rgba(0,0,0,0.7)';
    logContainer.style.color = 'white';
    logContainer.style.padding = '10px';
    logContainer.style.borderRadius = '5px';
    logContainer.style.fontSize = '12px';
    logContainer.style.maxWidth = '80%';
    logContainer.style.maxHeight = '30%';
    logContainer.style.overflow = 'auto';
    logContainer.id = 'touch-event-log';
    
    // Add close button
    const closeButton = document.createElement('button');
    closeButton.textContent = 'Close';
    closeButton.style.position = 'absolute';
    closeButton.style.top = '5px';
    closeButton.style.right = '5px';
    closeButton.style.padding = '3px 6px';
    closeButton.style.fontSize = '10px';
    closeButton.style.background = '#333';
    closeButton.style.border = 'none';
    closeButton.style.color = 'white';
    closeButton.style.borderRadius = '3px';
    closeButton.onclick = () => {
      document.body.removeChild(logContainer);
    };
    
    logContainer.appendChild(closeButton);
    
    // Add log content
    const logContent = document.createElement('div');
    logContent.id = 'touch-log-content';
    logContainer.appendChild(logContent);
    
    document.body.appendChild(logContainer);
    return logContent;
  };
  
  // Log events to the display
  const logElement = createLogDisplay();
  
  // Helper to add log entry
  const logEvent = (eventType, target, prevented) => {
    const entry = document.createElement('div');
    entry.style.marginBottom = '5px';
    entry.style.borderBottom = '1px solid rgba(255,255,255,0.2)';
    entry.style.paddingBottom = '3px';
    
    const time = new Date().toLocaleTimeString();
    let targetName = target.tagName.toLowerCase();
    if (target.id) targetName += `#${target.id}`;
    if (target.className) targetName += `.${target.className.split(' ')[0]}`;
    
    entry.innerHTML = `
      <span style="color: ${prevented ? 'red' : 'lightgreen'}">${time} - ${eventType}</span><br>
      <small>Target: ${targetName}</small>
    `;
    
    logElement.insertBefore(entry, logElement.firstChild);
    
    // Limit entries
    if (logElement.children.length > 20) {
      logElement.removeChild(logElement.lastChild);
    }
  };
  
  // Track touch events
  const touchEvents = ['touchstart', 'touchend', 'touchmove', 'touchcancel', 'click', 'mousedown', 'mouseup'];
  
  touchEvents.forEach(eventType => {
    document.addEventListener(eventType, (e) => {
      // Check if default prevented
      const prevented = e.defaultPrevented;
      logEvent(eventType, e.target, prevented);
      
      // For debugging purposes, log to console too
      console.log(`${eventType} on ${e.target.tagName}${e.target.className ? '.' + e.target.className : ''}`, {
        defaultPrevented: prevented,
        time: new Date().toLocaleTimeString(),
        target: e.target
      });
    }, { passive: true });
  });
};

/**
 * Test touch interactions on key elements
 * Adds visual indicators to test touch events
 */
export const testTouchInteractions = () => {
  // Create test UI
  const createTestUI = () => {
    const testContainer = document.createElement('div');
    testContainer.style.position = 'fixed';
    testContainer.style.top = '50%';
    testContainer.style.left = '50%';
    testContainer.style.transform = 'translate(-50%, -50%)';
    testContainer.style.zIndex = '9999';
    testContainer.style.backgroundColor = 'white';
    testContainer.style.padding = '20px';
    testContainer.style.borderRadius = '10px';
    testContainer.style.boxShadow = '0 4px 10px rgba(0,0,0,0.3)';
    testContainer.style.maxWidth = '90%';
    testContainer.style.width = '300px';
    testContainer.style.textAlign = 'center';
    
    testContainer.innerHTML = `
      <h3 style="margin-top: 0">Touch Interaction Test</h3>
      <p>Tap each element to test interactions:</p>
      <div style="display: flex; flex-direction: column; gap: 10px; margin: 15px 0;">
        <button id="test-button" style="padding: 10px; border-radius: 5px; background: #004d99; color: white; border: none;">Test Button</button>
        <a href="#" id="test-link" style="padding: 10px; text-decoration: none; color: #004d99;">Test Link</a>
        <div id="test-clickable" class="clickable" style="padding: 10px; background: #f0f0f0; border-radius: 5px; cursor: pointer;">Test Clickable Div</div>
        <label style="display: flex; align-items: center; padding: 10px;">
          <input type="checkbox" id="test-checkbox" style="margin-right: 10px;"> Test Checkbox
        </label>
        <label style="display: flex; align-items: center; padding: 10px;">
          <input type="radio" name="test-radio" id="test-radio" style="margin-right: 10px;"> Test Radio
        </label>
      </div>
      <div id="test-result" style="min-height: 40px; margin-top: 10px; font-size: 14px; color: #666;"></div>
      <button id="close-test" style="padding: 8px 15px; background: #333; color: white; border: none; border-radius: 5px; margin-top: 15px;">Close Test</button>
    `;
    
    document.body.appendChild(testContainer);
    return testContainer;
  };
  
  const testUI = createTestUI();
  const resultElement = testUI.querySelector('#test-result');
  
  // Add event listeners to test elements
  const testElements = [
    { id: 'test-button', name: 'Button' },
    { id: 'test-link', name: 'Link' },
    { id: 'test-clickable', name: 'Clickable div' },
    { id: 'test-checkbox', name: 'Checkbox' },
    { id: 'test-radio', name: 'Radio button' }
  ];
  
  testElements.forEach(elem => {
    const element = testUI.querySelector(`#${elem.id}`);
    
    element.addEventListener('click', (e) => {
      if (elem.id === 'test-link') {
        e.preventDefault(); // Prevent navigation for the test link
      }
      
      resultElement.innerHTML = `
        <div style="color: green; font-weight: bold;">✓ ${elem.name} clicked successfully!</div>
        <small>${new Date().toLocaleTimeString()}</small>
      `;
      
      // Highlight the result
      resultElement.style.backgroundColor = '#eaffea';
      resultElement.style.padding = '10px';
      resultElement.style.borderRadius = '5px';
      
      // Reset after 2 seconds
      setTimeout(() => {
        resultElement.style.backgroundColor = '';
        resultElement.style.padding = '';
      }, 2000);
    });
  });
  
  // Close button handler
  testUI.querySelector('#close-test').addEventListener('click', () => {
    document.body.removeChild(testUI);
  });
};

/**
 * Add this function to your index.js or App component
 * to test mobile interactions in development
 */
export const initMobileInteractionTesting = () => {
  if (process.env.NODE_ENV === 'development') {
    // Add floating action button to activate tests
    const testButton = document.createElement('button');
    testButton.textContent = '🔍 Test Mobile';
    testButton.style.position = 'fixed';
    testButton.style.bottom = '20px';
    testButton.style.right = '20px';
    testButton.style.zIndex = '9998';
    testButton.style.backgroundColor = '#004d99';
    testButton.style.color = 'white';
    testButton.style.border = 'none';
    testButton.style.borderRadius = '50%';
    testButton.style.width = '60px';
    testButton.style.height = '60px';
    testButton.style.boxShadow = '0 2px 5px rgba(0,0,0,0.3)';
    testButton.style.display = 'flex';
    testButton.style.alignItems = 'center';
    testButton.style.justifyContent = 'center';
    testButton.style.fontSize = '10px';
    testButton.style.textAlign = 'center';
    testButton.style.lineHeight = '1.2';
    
    testButton.addEventListener('click', () => {
      testTouchInteractions();
    });
    
    // Only add after DOM is ready
    if (document.readyState === 'complete') {
      document.body.appendChild(testButton);
    } else {
      window.addEventListener('DOMContentLoaded', () => {
        document.body.appendChild(testButton);
      });
    }
  }
};
