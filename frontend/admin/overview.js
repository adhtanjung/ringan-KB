// Admin Dashboard - Overview Page

document.addEventListener('DOMContentLoaded', function() {
    loadKnowledgeBaseStats();
    loadKnowledgeDistribution();
    loadRecentResponses();
    loadKnowledgeBaseHealth();
});

// Load knowledge base statistics
async function loadKnowledgeBaseStats() {
    try {
        // In a real implementation, fetch this data from your API
        // const data = await fetchData('/admin/kb-stats');
        
        // For demonstration, using mock data
        const data = {
            totalDocuments: 156,
            totalCategories: 3,
            averageDocLength: 245,
            lastUpdated: '2023-07-15T14:30:00Z'
        };
        
        const statsContainer = document.getElementById('kb-stats');
        statsContainer.innerHTML = `
            <div class="stat-item">
                <div class="stat-value">${data.totalDocuments}</div>
                <div class="stat-label">Documents</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${data.totalCategories}</div>
                <div class="stat-label">Categories</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${data.averageDocLength}</div>
                <div class="stat-label">Avg. Length</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${formatDate(data.lastUpdated).split(',')[0]}</div>
                <div class="stat-label">Last Updated</div>
            </div>
        `;
    } catch (error) {
        showError('kb-stats', 'Failed to load knowledge base statistics');
    }
}

// Load knowledge distribution chart
function loadKnowledgeDistribution() {
    try {
        // For demonstration, using mock data
        const data = {
            labels: ['Problems', 'Self-Assessments', 'Suggestions'],
            datasets: [{
                label: 'Number of Documents',
                data: [42, 68, 46],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        };
        
        const ctx = document.getElementById('knowledge-distribution-chart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: 'Knowledge Base Document Distribution'
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading knowledge distribution chart:', error);
    }
}

// Load recent AI responses
async function loadRecentResponses() {
    try {
        // For demonstration, using mock data
        const responses = [
            {
                id: 'resp1',
                query: 'How can I manage anxiety?',
                timestamp: '2023-07-15T14:30:00Z',
                sourcesUsed: 3
            },
            {
                id: 'resp2',
                query: 'What are symptoms of depression?',
                timestamp: '2023-07-15T13:45:00Z',
                sourcesUsed: 2
            },
            {
                id: 'resp3',
                query: 'Techniques for mindfulness meditation',
                timestamp: '2023-07-15T12:15:00Z',
                sourcesUsed: 4
            }
        ];
        
        const responsesContainer = document.getElementById('recent-responses');
        responsesContainer.innerHTML = responses.map(response => `
            <a href="response-analyzer.html?id=${response.id}" class="list-group-item list-group-item-action">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">${escapeHtml(response.query)}</h6>
                    <small>${formatDate(response.timestamp)}</small>
                </div>
                <small class="text-muted">Sources used: ${response.sourcesUsed}</small>
            </a>
        `).join('');
    } catch (error) {
        showError('recent-responses', 'Failed to load recent responses');
    }
}

// Load knowledge base health chart
function loadKnowledgeBaseHealth() {
    try {
        // For demonstration, using mock data
        const data = {
            labels: ['Coverage', 'Relevance', 'Freshness', 'Accuracy'],
            datasets: [{
                label: 'Current Score',
                data: [85, 78, 92, 88],
                fill: true,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgb(54, 162, 235)',
                pointBackgroundColor: 'rgb(54, 162, 235)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(54, 162, 235)'
            }]
        };
        
        const ctx = document.getElementById('kb-health-chart').getContext('2d');
        new Chart(ctx, {
            type: 'radar',
            data: data,
            options: {
                elements: {
                    line: {
                        borderWidth: 3
                    }
                },
                scales: {
                    r: {
                        angleLines: {
                            display: true
                        },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading knowledge base health chart:', error);
    }
}