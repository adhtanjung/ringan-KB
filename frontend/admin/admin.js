// Admin Dashboard - Common Functions

// API endpoint base URL - change this if your backend is hosted elsewhere
const API_BASE_URL = 'http://localhost:8000';

// Fetch data with error handling
async function fetchData(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error(`Error fetching data from ${endpoint}:`, error);
        throw error;
    }
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Create a loading spinner
function createLoadingSpinner() {
    return `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
}

// Show error message
function showError(container, message) {
    document.getElementById(container).innerHTML = `
        <div class="alert alert-danger">
            ${message}
        </div>
    `;
}

// Truncate text to specified length
function truncateText(text, maxLength = 100) {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
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

// Get color based on relevance score
function getRelevanceColor(score) {
    if (score >= 0.7) return 'relevance-high';
    if (score >= 0.4) return 'relevance-medium';
    return 'relevance-low';
}

// Toggle between list and graph views
document.addEventListener('DOMContentLoaded', function() {
    const viewButtons = document.querySelectorAll('[data-view]');
    if (viewButtons.length > 0) {
        viewButtons.forEach(button => {
            button.addEventListener('click', function() {
                const view = this.getAttribute('data-view');
                
                // Update active button
                viewButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Show selected view
                if (view === 'list') {
                    document.getElementById('list-view').style.display = 'block';
                    document.getElementById('graph-view').style.display = 'none';
                } else if (view === 'graph') {
                    document.getElementById('list-view').style.display = 'none';
                    document.getElementById('graph-view').style.display = 'block';
                    // Initialize graph if needed
                    if (typeof initializeGraph === 'function') {
                        initializeGraph();
                    }
                }
            });
        });
    }
});