// Standalone chatbot script that will be loaded separately
function initializeRAGChatbot() {
  // Only run once
  if (window.RAGChatbotLoaded) return;
  window.RAGChatbotLoaded = true;

  // Create the chatbot container
  const container = document.createElement('div');
  container.id = 'rag-chatbot-standalone';
  container.innerHTML = `
    <div id="rag-chatbot-container" class="rag-chatbot-container closed">
      <div class="rag-chat-header">
        <h3>Book Assistant</h3>
        <button id="rag-toggle-btn" class="rag-toggle-btn">+</button>
      </div>
      <div id="rag-chat-body" class="rag-chat-body" style="display: none;">
        <div id="rag-chat-messages" class="rag-chat-messages"></div>
        <div class="rag-input-area">
          <textarea id="rag-question-input" class="rag-question-input" placeholder="Ask a question about the book..."></textarea>
          <button id="rag-send-btn" class="rag-send-btn">Send</button>
        </div>
      </div>
    </div>
  `;
  document.body.appendChild(container);

  // Add CSS styles
  const style = document.createElement('style');
  style.textContent = `
    .rag-chatbot-container {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 350px;
      max-height: 500px;
      border: 1px solid #ccc;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      background: white;
      z-index: 1000;
      font-family: Arial, sans-serif;
    }

    .rag-chat-header {
      background: #4f5cf5;
      color: white;
      padding: 12px 15px;
      border-top-left-radius: 10px;
      border-top-right-radius: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      font-weight: 500;
    }

    .rag-chat-header h3 {
      margin: 0;
      font-size: 16px;
    }

    .rag-toggle-btn {
      background: none;
      border: none;
      color: white;
      font-size: 20px;
      cursor: pointer;
      padding: 0;
      width: 24px;
      height: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .rag-chat-body {
      display: flex;
      flex-direction: column;
      height: 400px;
    }

    .rag-chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 15px;
      background: #f9f9f9;
      display: flex;
      flex-direction: column;
      max-height: 300px;
    }

    .rag-chat-messages::-webkit-scrollbar {
      width: 6px;
    }

    .rag-chat-messages::-webkit-scrollbar-track {
      background: #f1f1f1;
      border-radius: 10px;
    }

    .rag-chat-messages::-webkit-scrollbar-thumb {
      background: #c5c5c5;
      border-radius: 10px;
    }

    .rag-chat-messages::-webkit-scrollbar-thumb:hover {
      background: #a8a8a8;
    }

    .rag-message {
      margin-bottom: 10px;
      padding: 10px 14px;
      border-radius: 18px;
      max-width: 80%;
      word-wrap: break-word;
      box-shadow: 0 1px 1px rgba(0,0,0,0.1);
      font-size: 14px;
      line-height: 1.4;
    }

    .rag-user-message {
      background: #4f5cf5;
      color: white;
      align-self: flex-end;
      margin-left: auto;
      margin-right: 0;
      text-align: right;
      border-bottom-right-radius: 4px;
      border-bottom-left-radius: 18px;
    }

    .rag-assistant-message {
      background: #e3f2fd;
      color: #333;
      align-self: flex-start;
      margin-right: auto;
      margin-left: 0;
      text-align: left;
      border-bottom-left-radius: 4px;
      border-bottom-right-radius: 18px;
    }

    .rag-typing-indicator {
      color: #888;
      font-style: italic;
      padding: 8px 12px;
    }

    .rag-input-area {
      display: flex;
      padding: 8px 10px;
      border-top: 1px solid #e0e0e0;
      background: white;
    }

    .rag-question-input {
      flex: 1;
      padding: 10px 12px;
      border: 1px solid #e0e0e0;
      border-radius: 18px;
      margin-right: 8px;
      resize: none;
      overflow: hidden;
      font-family: Arial, sans-serif;
      font-size: 14px;
      outline: none;
    }

    .rag-question-input:focus {
      border-color: #4f5cf5;
      box-shadow: 0 0 0 1px #4f5cf5;
    }

    .rag-send-btn {
      padding: 10px 16px;
      background: #4f5cf5;
      color: white;
      border: none;
      border-radius: 18px;
      cursor: pointer;
      font-weight: 500;
    }

    .rag-send-btn:hover:not(:disabled) {
      background: #3a46c4;
    }

    .rag-send-btn:disabled {
      background: #cccccc;
      cursor: not-allowed;
    }
  `;
  document.head.appendChild(style);

  // Initialize chatbot functionality
  let isOpen = false;
  let isLoading = false;

  // DOM elements
  const chatContainer = document.getElementById('rag-chat-container');
  const toggleBtn = document.getElementById('rag-toggle-btn');
  const chatBody = document.getElementById('rag-chat-body');
  const chatMessages = document.getElementById('rag-chat-messages');
  const questionInput = document.getElementById('rag-question-input');
  const sendBtn = document.getElementById('rag-send-btn');

  // Add initial message
  const initialMessageDiv = document.createElement('div');
  initialMessageDiv.className = 'rag-message rag-assistant-message';
  initialMessageDiv.textContent = 'Hello! I\'m your book assistant. Ask me anything about the book content!';
  chatMessages.appendChild(initialMessageDiv);
  scrollToBottom();

  // Toggle chat window
  function toggleChat() {
    isOpen = !isOpen;
    chatBody.style.display = isOpen ? 'block' : 'none';
    toggleBtn.textContent = isOpen ? '−' : '+';
  }

  toggleBtn.addEventListener('click', toggleChat);

  // Add message to chat
  function addMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `rag-message rag-${sender}-message`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
  }

  // Scroll to bottom of chat
  function scrollToBottom() {
    chatMessages.scrollTo({
      top: chatMessages.scrollHeight,
      behavior: 'smooth'
    });
  }

  // Add typing indicator
  function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.id = 'rag-typing-indicator';
    typingDiv.className = 'rag-message assistant-message';
    typingDiv.innerHTML = '<div class="rag-typing-indicator">Thinking...</div>';
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
  }

  // Remove typing indicator
  function removeTypingIndicator() {
    const typingIndicator = document.getElementById('rag-typing-indicator');
    if (typingIndicator) {
      typingIndicator.remove();
    }
  }

  // Send message function
  async function sendMessage() {
    const question = questionInput.value.trim();
    if (!question || isLoading) return;

    // Add user message
    addMessage('user', question);
    questionInput.value = '';

    // Show loading state
    isLoading = true;
    sendBtn.disabled = true;
    addTypingIndicator();

    try {
      // Ensure proper URL construction without double slashes
      const apiUrl = window.RAG_CHATBOT_API_URL || 'http://localhost:8000';
      const cleanApiUrl = apiUrl.replace(/\/+$/, ''); // Remove trailing slashes
      const fullUrl = cleanApiUrl + '/ask';

      const response = await fetch(fullUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question })
      });

      if (!response.ok) {
        throw new Error('Server error: ' + response.status);
      }

      const data = await response.json();

      // Remove typing indicator and add response
      removeTypingIndicator();
      // The /ask endpoint returns 'answer' field, not 'response'
      const messageText = data.answer || data.response || 'Sorry, I could not generate a response.';
      addMessage('assistant', messageText);
    } catch (error) {
      removeTypingIndicator();
      addMessage('assistant', 'Sorry, I encountered an error processing your question. Please try again.');
      console.error('Error sending message:', error);
    } finally {
      isLoading = false;
      sendBtn.disabled = false;
    }
  }

  // Event listeners
  sendBtn.addEventListener('click', sendMessage);

  questionInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Initialize
  scrollToBottom();
}

// Initialize the chatbot when DOM is ready, with fallback for different loading scenarios
if (document.readyState === 'loading') {
  // DOM is still loading, wait for it
  document.addEventListener('DOMContentLoaded', initializeRAGChatbot);
} else {
  // DOM is already loaded, initialize immediately
  // Add a small delay to ensure all other scripts have loaded
  setTimeout(initializeRAGChatbot, 100);
}

// Also try to initialize when the page is fully loaded
window.addEventListener('load', function() {
  setTimeout(initializeRAGChatbot, 50); // Small delay to ensure everything is ready
});