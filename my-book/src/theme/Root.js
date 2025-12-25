import React, { useEffect } from 'react';

// Root component that wraps the entire app
export default function Root({ children }) {
  useEffect(() => {
    // Set the API URL from the Docusaurus config
    // Access the site config to get the custom field
    const setApiUrl = () => {
      // Try to access the Docusaurus site config to get the API URL
      // In the browser, we can access Docusaurus data through global variables
      if (typeof window !== 'undefined' && window.__DOCUSAURUS__) {
        const siteConfig = window.__DOCUSAURUS__.siteConfig;
        if (siteConfig && siteConfig.customFields && siteConfig.customFields.ragChatbotApiUrl) {
          window.RAG_CHATBOT_API_URL = siteConfig.customFields.ragChatbotApiUrl;
        } else {
          window.RAG_CHATBOT_API_URL = 'http://localhost:8000'; // Default
        }
      } else {
        // For development, try to set from window or default
        window.RAG_CHATBOT_API_URL = window.RAG_CHATBOT_API_URL || 'http://localhost:8000';
      }
    };

    setApiUrl();

    // Dynamically load the chatbot script after the page has loaded
    const script = document.createElement('script');
    script.src = '/rag-chatbot.js'; // This will load from the static folder
    script.async = true;
    document.head.appendChild(script);

    // Cleanup function
    return () => {
      // Remove script when component unmounts
      document.head.removeChild(script);
    };
  }, []);

  return (
    <>
      {children}
    </>
  );
}