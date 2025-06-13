# Ringan Mental Health AI Assistant

A comprehensive AI assistant for mental health support, utilizing a structured knowledge base with retrieval-augmented generation (RAG) capabilities. The assistant guides users through self-assessments, provides relevant suggestions, and collects feedback to improve future interactions.

## 🌟 Features

- **Interactive Self-Assessments**: Guides users through questions to identify and understand their concerns
- **Personalized Suggestions**: Offers coping mechanisms and resources based on identified problems
- **Feedback Collection**: Gathers user feedback on suggestion effectiveness to improve future interactions
- **Structured Knowledge Base**: SQLAlchemy-based database models for mental health problems, self-assessments, suggestions, and feedback
- **Vector Database for RAG**: HuggingFace embeddings and Chroma vector database for retrieval-augmented generation to enhance contextual understanding
- **Visual Reporting**: Generates HTML reports showing knowledge base usage and effectiveness
- **Modern Web Interface**: User-friendly Next.js frontend for interacting with the AI assistant

## 📋 Requirements

- Python 3.8 or higher
- Node.js 18+ (for Next.js frontend)
- Dependencies listed in `requirements.txt`

## 🔧 Installation

### Backend Setup

1. Clone and enter the repository:
```bash
git clone <repository-url>
cd ringan-KB
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Frontend Setup

1. Navigate to the Next.js frontend directory:
```bash
cd nextjs-frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

## 🚀 Running the Application

### Start the Backend API

For development with auto-reload:
```bash
uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
```

Alternatively, you can use the run script:
```bash
# On macOS/Linux
./run.sh 
# Then select option 4

# On Windows
.\run.bat
# Then select option 4
```
The API will be available at: http://127.0.0.1:8000

### Start the Frontend Development Server

```bash
cd nextjs-frontend
npm run dev
```
Access the web interface at: http://localhost:3000

## 📊 Knowledge Base Reports

Generate a visual report of the knowledge base usage:
```bash
python ringan_kb.py --report
```
This creates an HTML report in the `reports` directory.

## 🏗️ Project Structure

- **data/**: Knowledge base data and vector database
- **src/**: Core application logic
  - **ai_orchestration.py**: Manages conversation flow
  - **api.py**: FastAPI backend endpoints
  - **app.py**: Main application entry point
  - **db_schema.py**: SQLAlchemy database models
  - **vector_db_preparation.py**: Text embeddings for RAG
- **nextjs-frontend/**: Modern web interface built with Next.js
- **scripts/**: Development and maintenance utilities
- **reports/**: Generated usage reports

## 🔄 API Documentation

API documentation available at: http://127.0.0.1:8000/docs

### Key Endpoints

#### Chat
Send a message and get an AI response.

```http
POST /chat
```

**Request Body:**
```json
{
  "message": "I'm feeling anxious today",
  "session_id": "optional_session_id"
}
```

#### Feedback
Submit feedback about an AI response.

```http
POST /feedback
```

**Request Body:**
```json
{
  "session_id": "session_id",
  "message_id": "msg_id",
  "rating": 4,
  "comments": "This suggestion was helpful"
}
```
