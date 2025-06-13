# Integrating Next.js Frontend with Ringan KB Backend

This document provides instructions for integrating the new Next.js frontend with the existing Ringan KB backend system.

## Overview

The Next.js frontend is designed to work seamlessly with the existing FastAPI backend. It provides a modern, responsive user interface with three main sections:

1. **Mental Health Features Page** - User-facing interface for interacting with the AI assistant
2. **Knowledge Base Report Page** - Admin interface for monitoring KB usage and effectiveness
3. **AI Flow Visualization Page** - Admin interface for visualizing the AI's processing flow

## Setup Instructions

### 1. Install Dependencies

```bash
cd nextjs-frontend
npm install
```

### 2. Configure API Endpoint

The frontend is configured to connect to the backend at `http://localhost:8000`. If your backend runs on a different URL, update the `API_BASE_URL` in `/src/lib/api.ts`.

### 3. Start the Development Server

```bash
npm run dev
```

This will start the Next.js development server on port 8080 (http://localhost:8080).

### 4. Start the Backend Server

In a separate terminal, start the Ringan KB backend:

```bash
python ringan_kb.py --api
```

## Integration Points

### API Endpoints

The Next.js frontend uses the following API endpoints from the Ringan KB backend:

- `/problems` - Get list of mental health problems
- `/suggestions` - Get suggestions for problems
- `/self-assessments` - Get self-assessment questions
- `/chat` - Send messages to the AI assistant
- `/feedback` - Submit feedback on AI responses
- `/kb-stats` - Get knowledge base statistics
- `/kb-usage-report` - Get detailed KB usage reports

### XLSX Data Visualization

The frontend explicitly shows how data from XLSX sheets impacts the AI system:

- **Problems.xlsx** - Displayed in the Problems list with last update timestamps
- **SelfAssessment.xlsx** - Powers the interactive assessments with source indicators
- **Suggestions.xlsx** - Provides the suggestions with KB source references
- **FeedbackPrompts.xlsx** - Guides the feedback collection process
- **NextActions.xlsx** - Influences conversation flow
- **FinetuningExamples.xlsx** - Shapes the AI's conversational style

## Extending the Frontend

The Next.js frontend is built with modularity in mind. To add new features:

1. Create new components in `/src/components`
2. Add new pages in `/src/app`
3. Extend API functions in `/src/lib/api.ts`

## Production Deployment

To build the frontend for production:

```bash
npm run build
npm start
```

For production deployment, consider using a service like Vercel, Netlify, or a containerized solution with Docker.

## Troubleshooting

- **CORS Issues**: Ensure the backend has CORS configured to allow requests from the frontend origin
- **API Connection Errors**: Verify the backend is running and accessible at the configured URL
- **Missing Data**: Check that the knowledge base has been properly set up with `python ringan_kb.py --setup`