// Client module for RAG Chatbot - this will be loaded by Docusaurus

// Create and inject the chatbot when the module is loaded
if (typeof document !== 'undefined') {
  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeChatbot);
  } else {
    initializeChatbot();
  }
}

function initializeChatbot() {
  // Check if chatbot is already injected to avoid duplicates
  if (document.getElementById('rag-chatbot-root')) {
    return;
  }

  // Create a container for the chatbot
  const chatbotContainer = document.createElement('div');
  chatbotContainer.id = 'rag-chatbot-root';
  document.body.appendChild(chatbotContainer);

  // The actual rendering will be handled by the component itself
  // when React processes the DOM element
}

// This module doesn't need to export anything specific for the client module system
// The initialization happens automatically when the module is loaded