# Next.js Frontend for Mental Health AI System

A modern, interactive web application frontend for the Ringan mental health AI system. This frontend serves as the primary interface for users to engage with mental health features and provides key administrative insights into the AI's operation and the underlying knowledge bases.

## Technology Stack

- **Framework:** Next.js (App Router)
- **Styling:** Tailwind CSS
- **UI Components:** Shadcn UI
- **Data Fetching:** TanStack React Query
- **State Management:** Zustand
- **Visualization:** React Flow

## Core Principles

- **Responsiveness:** Full adaptability across devices
- **Accessibility (A11y):** WCAG compliant
- **Performance:** Fast loading and smooth interactions
- **Modularity:** Clean, scalable, maintainable codebase
- **Security:** Proper authentication/authorization with backend

## Key Features

### Mental Health Features & Knowledge Base Details Page (User-Facing)

- AI Chat Interface with feedback collection
- Interactive Self-Assessments from XLSX-driven knowledge base
- Personalized Suggestions & Interventions
- KB Overview Section explaining XLSX sheet roles

### Knowledge Base Report Page (Admin-Facing)

- XLSX Data Status showing last import date/time and entry counts
- KB Coverage visualizations
- Usage Statistics graphs
- Feedback Analysis
- KB Versioning & Impact tracking

### AI Flow Visualization Page (Admin-Facing)

- Interactive diagram showing AI processing flow
- Visual representation of knowledge retrieval from XLSX sheets
- Dynamic KB influence demonstration

## Getting Started

```bash
# Install dependencies
npm install

# Run the development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Integration with Backend

This frontend integrates with the FastAPI backend at `http://localhost:8000` for all data operations related to the mental health knowledge base.