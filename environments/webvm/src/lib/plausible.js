/**
 * Plausible Analytics Helper
 * 
 * Provides privacy-friendly analytics tracking for WebVM
 * using Plausible Analytics (if configured)
 * 
 * Note: All functions handle SSR gracefully by checking for window/browser environment
 */

// Browser detection helper
const isBrowser = typeof window !== 'undefined';

/**
 * Try to send an event to Plausible Analytics
 * @param {string} eventName - The name of the event to track
 * @param {Object} props - Optional event properties
 */
export function tryPlausible(eventName, props = {}) {
  // Skip during SSR
  if (!isBrowser) return;
  
  try {
    // Check if Plausible is available
    if (window.plausible) {
      window.plausible(eventName, { props });
      console.log(`[Analytics] Event tracked: ${eventName}`, props);
    } else {
      // Plausible not available, log to console in development
      if (import.meta.env?.DEV) {
        console.log(`[Analytics] Would track: ${eventName}`, props);
      }
    }
  } catch (error) {
    // Silently fail - analytics should never break the app
    console.warn('[Analytics] Failed to track event:', error);
  }
}

/**
 * Track a page view
 * @param {string} url - The URL to track
 */
export function trackPageView(url) {
  tryPlausible('pageview', { url });
}

/**
 * Track a custom event
 * @param {string} category - Event category
 * @param {string} action - Event action
 * @param {string} label - Event label (optional)
 * @param {number} value - Event value (optional)
 */
export function trackEvent(category, action, label = null, value = null) {
  const props = {
    category,
    action,
  };
  
  if (label) props.label = label;
  if (value !== null) props.value = value;
  
  tryPlausible('custom_event', props);
}

/**
 * Track VM interaction events
 * @param {string} interactionType - Type of interaction (e.g., 'command', 'file_open', 'process_start')
 * @param {Object} details - Additional details about the interaction
 */
export function trackVMInteraction(interactionType, details = {}) {
  tryPlausible('vm_interaction', {
    type: interactionType,
    ...details,
  });
}

/**
 * Track avatar interaction events
 * @param {string} interactionType - Type of avatar interaction
 * @param {Object} details - Additional details
 */
export function trackAvatarInteraction(interactionType, details = {}) {
  tryPlausible('avatar_interaction', {
    type: interactionType,
    ...details,
  });
}

/**
 * Track terminal command execution
 * @param {string} command - The command executed (sanitized)
 * @param {boolean} success - Whether the command succeeded
 */
export function trackCommand(command, success = true) {
  // Sanitize command to remove sensitive data
  const sanitizedCommand = sanitizeCommand(command);
  
  tryPlausible('terminal_command', {
    command: sanitizedCommand,
    success,
  });
}

/**
 * Sanitize command to remove sensitive information
 * @param {string} command - The raw command
 * @returns {string} - Sanitized command
 */
function sanitizeCommand(command) {
  // Remove potential passwords, tokens, keys
  let sanitized = command.replace(/password[=:\s]+\S+/gi, 'password=***');
  sanitized = sanitized.replace(/token[=:\s]+\S+/gi, 'token=***');
  sanitized = sanitized.replace(/key[=:\s]+\S+/gi, 'key=***');
  sanitized = sanitized.replace(/api[_-]?key[=:\s]+\S+/gi, 'api_key=***');
  
  // Truncate if too long
  if (sanitized.length > 100) {
    sanitized = sanitized.substring(0, 97) + '...';
  }
  
  return sanitized;
}

/**
 * Track performance metrics
 * @param {string} metric - Metric name
 * @param {number} value - Metric value
 * @param {string} unit - Unit of measurement (optional)
 */
export function trackPerformance(metric, value, unit = 'ms') {
  tryPlausible('performance', {
    metric,
    value,
    unit,
  });
}

/**
 * Track errors
 * @param {string} errorType - Type of error
 * @param {string} message - Error message (sanitized)
 */
export function trackError(errorType, message) {
  // Sanitize error message to remove sensitive paths or data
  const sanitizedMessage = message.substring(0, 200);
  
  tryPlausible('error', {
    type: errorType,
    message: sanitizedMessage,
  });
}

/**
 * Initialize analytics tracking
 * @param {Object} config - Configuration options
 */
export function initializeAnalytics(config = {}) {
  // Skip during SSR
  if (!isBrowser) return;
  
  const {
    domain = window.location.hostname,
    apiHost = 'https://plausible.io',
    trackLocalhost = false,
  } = config;
  
  // Don't track localhost unless explicitly enabled
  if (!trackLocalhost && (
    window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1'
  )) {
    console.log('[Analytics] Localhost tracking disabled');
    return;
  }
  
  // Load Plausible script if not already loaded
  if (!window.plausible && !document.querySelector('script[data-domain]')) {
    const script = document.createElement('script');
    script.defer = true;
    script.dataset.domain = domain;
    script.src = `${apiHost}/js/script.js`;
    document.head.appendChild(script);
    
    console.log('[Analytics] Plausible script loaded');
  }
}

// Export all functions as default object as well
export default {
  tryPlausible,
  trackPageView,
  trackEvent,
  trackVMInteraction,
  trackAvatarInteraction,
  trackCommand,
  trackPerformance,
  trackError,
  initializeAnalytics,
};
