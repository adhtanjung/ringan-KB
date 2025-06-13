// Mental Health AI Assistant - Frontend JavaScript

// API endpoint base URL - change this if your backend is hosted elsewhere
const API_BASE_URL = 'http://localhost:8000';

// Global variables
// At the top of your file, after your other global variables
let currentSessionId = null;
let selectedProblemId = null;
let lastUserMessage = null;
let lastAiResponse = null;
let chatMessagesElement = null;

// DOM Elements
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the application
    initApp();
    
    // Initialize the chatMessages element reference
    chatMessagesElement = document.getElementById('chat-messages');
    
    // Set up event listeners
    document.getElementById('send-button').addEventListener('click', sendMessage);
    document.getElementById('message-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    document.getElementById('submit-feedback').addEventListener('click', submitFeedback);

    // Enable feedback button only when there's text
    document.getElementById('feedback-text').addEventListener('input', function() {
        document.getElementById('submit-feedback').disabled = this.value.trim() === '';
    });
});

// Initialize the application
async function initApp() {
    try {
        // Load problems list
        await loadProblems();

        // Initial greeting message is already in the HTML
    } catch (error) {
        console.error('Error initializing app:', error);
        addSystemMessage('Error connecting to the server. Please try again later.');
    }
}

// Load mental health problems from API
// Add client-side caching for problems and suggestions
const cache = {
    problems: null,
    suggestions: {}
};

// Update loadProblems function to use cache
async function loadProblems() {
    try {
        // Check cache first
        if (cache.problems) {
            displayProblems(cache.problems);
            return cache.problems;
        }

        const response = await fetch(`${API_BASE_URL}/problems`);
        if (!response.ok) {
            throw new Error(`API responded with status: ${response.status}`);
        }

        const problems = await response.json();

        // Store in cache
        cache.problems = problems;

        displayProblems(problems);
        return problems;
    } catch (error) {
        console.error('Error loading problems:', error);
        document.getElementById('problems-list').innerHTML = `<div class="alert alert-danger">Error loading problems: ${error.message}</div>`;
        return [];
    }
}

// Update loadSuggestions function to use cache
async function loadSuggestions(problemId) {
    try {
        // Check cache first
        if (cache.suggestions[problemId]) {
            displaySuggestions(cache.suggestions[problemId]);
            return;
        }

        const response = await fetch(`${API_BASE_URL}/suggestions?problem_id=${problemId}`);
        if (!response.ok) {
            throw new Error(`API responded with status: ${response.status}`);
        }

        const suggestions = await response.json();

        // Store in cache
        cache.suggestions[problemId] = suggestions;

        displaySuggestions(suggestions);
    } catch (error) {
        console.error('Error loading suggestions:', error);
        document.getElementById('suggestions-list').innerHTML = `<div class="alert alert-danger">Error loading suggestions: ${error.message}</div>`;
    }
}

// Display problems in the sidebar
function displayProblems(problems) {
    const problemsList = document.getElementById('problems-list');

    if (problems.length === 0) {
        problemsList.innerHTML = '<p class="text-muted">No problems found</p>';
        return;
    }

    problemsList.innerHTML = problems.map(problem => `
        <button class="list-group-item list-group-item-action problem-item"
                data-id="${problem.id}">
            ${problem.problem_name}
        </button>
    `).join('');

    // Add click event listeners to problem items
    document.querySelectorAll('.problem-item').forEach(item => {
        item.addEventListener('click', async () => {
            // Highlight selected problem
            document.querySelectorAll('.problem-item').forEach(p =>
                p.classList.remove('active'));
            item.classList.add('active');

            // Store selected problem ID
            selectedProblemId = item.dataset.id;

            // Load suggestions for this problem
            await loadSuggestions(selectedProblemId);

            // Inform the AI about the selected problem
            if (currentSessionId) {
                addUserMessage(`I'd like to talk about ${item.textContent.trim()}`);
                await sendToAI(`I'd like to talk about the mental health problem: ${item.textContent.trim()}`);
            }
        });
    });
}

// Load suggestions for a specific problem
async function loadSuggestions(problemId) {
    try {
        const response = await fetch(`${API_BASE_URL}/suggestions?problem_id=${problemId}`);
        if (!response.ok) throw new Error('Failed to fetch suggestions');

        const suggestions = await response.json();
        displaySuggestions(suggestions);
    } catch (error) {
        console.error('Error loading suggestions:', error);
        document.getElementById('suggestions-list').innerHTML =
            `<div class="alert alert-danger">Failed to load suggestions: ${error.message}</div>`;
    }
}

// Display suggestions in the sidebar
function displaySuggestions(suggestions) {
    const suggestionsList = document.getElementById('suggestions-list');

    if (suggestions.length === 0) {
        suggestionsList.innerHTML = '<p class="text-muted">No suggestions available</p>';
        return;
    }

    suggestionsList.innerHTML = suggestions.map(suggestion => `
        <div class="list-group-item suggestion-item" data-id="${suggestion.suggestion_id}">
            ${suggestion.suggestion_text}
        </div>
    `).join('');

    // Add click event listeners to suggestions
    document.querySelectorAll('.suggestion-item').forEach(item => {
        item.addEventListener('click', () => {
            // Add the suggestion to the chat input
            document.getElementById('message-input').value =
                `Let me try this suggestion: ${item.textContent.trim()}`;
            document.getElementById('message-input').focus();
        });
    });
}

// Send a message to the AI
async function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (message === '') return;

    // Display user message in chat
    addUserMessage(message);

    // Clear input field
    messageInput.value = '';

    // Send to AI and get response
    await sendToAI(message);
}

// Send message to AI API
// 5. Frontend Optimization
//
// Add Loading States and Improve UX

// Add this function to show a more detailed loading state
function updateLoadingState(message) {
    const typingIndicator = document.querySelector('.typing-indicator');
    if (typingIndicator) {
        const statusElement = typingIndicator.querySelector('.status-message') || document.createElement('div');
        statusElement.className = 'status-message';
        statusElement.textContent = message;
        typingIndicator.appendChild(statusElement);
    }
}

// Update the sendToAI function
async function sendToAI(message) {
    addTypingIndicator();
    updateLoadingState('Connecting to AI...');

    try {
        const payload = {
            message: message,
            session_id: currentSessionId,
            context: {
                selected_problem_id: selectedProblemId
            }
        };

        updateLoadingState('Processing your message...');
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`API responded with status: ${response.status}`);
        }

        updateLoadingState('Receiving response...');
        const data = await response.json();

        // Update the session ID if provided
        if (data.session_id) {
            currentSessionId = data.session_id;
            document.getElementById('session-id').textContent = `Session ID: ${currentSessionId}`;
        }

        // Store the last AI response for feedback
        lastAiResponse = data.response;

        // Display the AI's response
        addAIMessage(data.response, data.metadata);

        // Enable the feedback button after receiving a response
        document.getElementById('submit-feedback').disabled = false;

    } catch (error) {
        console.error('Error sending message to AI:', error);
        removeTypingIndicator();
        addSystemMessage(`Error: ${error.message}. Please try again.`);
    }
}

// Submit feedback to the API
async function submitFeedback() {
    const feedbackText = document.getElementById('feedback-text').value.trim();
    const feedbackResult = document.getElementById('feedback-result');

    if (feedbackText === '' || !currentSessionId) return;

    try {
        feedbackResult.innerHTML = '<div class="spinner-border spinner-border-sm text-primary" role="status"></div> Sending feedback...';

        // Prepare request body
        const requestBody = {
            feedback: feedbackText,
            session_id: currentSessionId,
            user_message: lastUserMessage,
            ai_response: lastAiResponse,
            problem_id: selectedProblemId
        };

        // Send request to API
        const response = await fetch(`${API_BASE_URL}/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        // Parse response
        const data = await response.json();

        // Clear feedback text
        document.getElementById('feedback-text').value = '';
        document.getElementById('submit-feedback').disabled = true;

        // Show success message
        feedbackResult.innerHTML = `<div class="alert alert-success">Thank you for your feedback!</div>`;

        // Clear feedback message after 3 seconds
        setTimeout(() => {
            feedbackResult.innerHTML = '';
        }, 3000);

    } catch (error) {
        console.error('Error submitting feedback:', error);
        feedbackResult.innerHTML = `<div class="alert alert-danger">Error submitting feedback: ${error.message}</div>`;
    }
}

// Helper functions for UI updates
function addUserMessage(message) {
    // Replace this line
    // const chatMessages = document.getElementById('chat-messages');
    // With this
    chatMessagesElement.innerHTML += `
        <div class="message user-message">
            <div class="message-content">${escapeHtml(message)}</div>
        </div>
    `;
    scrollToBottom();
}

// Similarly update addAIMessage, addSystemMessage, and any other function
// that uses document.getElementById('chat-messages')
function addAIMessage(message, metadata = {}) {
    removeTypingIndicator();

    const messageElement = document.createElement('div');
    messageElement.className = 'message ai-message';

    // Format the main message
    const formattedMessage = formatMessage(message);
    messageElement.innerHTML = `
        <div class="message-content">${formattedMessage}</div>
    `;

    // If we have source documents, display them
    if (metadata && metadata.source_documents && metadata.source_documents.length > 0) {
        const sourcesContainer = document.createElement('div');
        sourcesContainer.className = 'sources-container';
        sourcesContainer.innerHTML = '<h4>Knowledge Base Sources:</h4>';

        const sourcesList = document.createElement('ul');
        sourcesList.className = 'sources-list';

        metadata.source_documents.forEach((doc, index) => {
            const sourceItem = document.createElement('li');
            sourceItem.className = 'source-item';

            // Extract and display metadata if available
            let metadataText = '';
            if (doc.metadata) {
                if (doc.metadata.problem_name) {
                    metadataText += `<strong>Problem:</strong> ${escapeHtml(doc.metadata.problem_name)}<br>`;
                }
                if (doc.metadata.suggestion_text) {
                    metadataText += `<strong>Suggestion:</strong> ${escapeHtml(doc.metadata.suggestion_text)}<br>`;
                }
                if (doc.metadata.source_type) {
                    metadataText += `<strong>Type:</strong> ${escapeHtml(doc.metadata.source_type)}<br>`;
                }
            }

            // Display content excerpt (first 150 chars)
            const contentExcerpt = doc.content ? escapeHtml(doc.content.substring(0, 150)) + (doc.content.length > 150 ? '...' : '') : 'No content';

            sourceItem.innerHTML = `
                <div class="source-header">Source ${index + 1}</div>
                <div class="source-metadata">${metadataText}</div>
                <div class="source-content">${contentExcerpt}</div>
            `;

            sourcesList.appendChild(sourceItem);
        });

        sourcesContainer.appendChild(sourcesList);
        messageElement.appendChild(sourcesContainer);
    }

    // Add this line to define chatMessages
    const chatMessages = document.getElementById('chat-messages');
    
    chatMessages.appendChild(messageElement);
    scrollToBottom();
}

function addSystemMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML += `
        <div class="message system-message">
            <div class="message-content">${message}</div>
        </div>
    `;
    scrollToBottom();
}

function addTypingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML += `
        <div id="typing-indicator" class="message ai-message">
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    scrollToBottom();
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) typingIndicator.remove();
}

function scrollToBottom() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Format message with markdown-like syntax
function formatMessage(message) {
    // Replace newlines with <br>
    let formatted = message.replace(/\n/g, '<br>');

    // Bold text between ** **
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic text between * *
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');

    return formatted;
}

// Escape HTML to prevent XSS
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}