# Mental Health AI Assistant

This project implements an AI assistant for mental health support, utilizing a structured knowledge base derived from Excel data. The assistant guides users through self-assessments, provides relevant suggestions, collects feedback, and leverages fine-tuning examples for enhanced conversational capabilities.

## Features

- Data Preprocessing : Clean and standardize data from Excel files, handling missing values and ensuring data quality.
- Structured Knowledge Base : SQLAlchemy-based database models for mental health problems, self-assessments, suggestions, feedback prompts, and next actions.
- Vector Database for RAG : Preparation of text embeddings for retrieval-augmented generation to enhance contextual understanding.
- LLM Fine-tuning Data : Formats knowledge base content for OpenAI and Hugging Face fine-tuning workflows.
- AI Orchestration : Integrates structured database, vector database, and fine-tuned LLM to manage conversation flow.
- Interactive Self-Assessments : Guides users through questions to identify and understand their concerns.
- Personalized Suggestions : Offers coping mechanisms and resources based on identified problems.
- Feedback Mechanism : Collects user feedback on suggestion effectiveness to improve future interactions.

## Project Structure

- data/ : Contains the missing_values_updated.xlsx file with mental health knowledge base data.
- src/ : Contains the core application logic:
  - app.py : Main application entry point for loading and displaying knowledge base data.
  - data_loader.py : Handles loading and parsing data from the Excel file into model objects.
  - data_preprocessing.py : Cleans and standardizes data from Excel files.
  - db_schema.py : Defines SQLAlchemy models for the structured knowledge base.
  - vector_db_preparation.py : Prepares text embeddings for retrieval-augmented generation.
  - finetuning_preparation.py : Formats data for LLM fine-tuning workflows.
  - ai_orchestration.py : Integrates components to manage conversation flow.
  - models.py : Defines data structures for the knowledge base.
- knowledgebase_mh.csv : CSV file containing action reference data for coaching sessions.
- requirements.txt : Lists Python dependencies.

## Dependencies

- pandas==2.2.3
- openpyxl==3.1.2
  Additional dependencies for full implementation (not yet in requirements.txt):

- SQLAlchemy (for database operations)
- sentence-transformers (for text embeddings)
- langchain (for AI orchestration)

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ringan-KB
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Prepare the Data
1. Place your Excel file (`missing_values_updated.xlsx`) in the `data/` directory
2. Run the data preprocessing script:
   ```bash
   python -m src.data_preprocessing
   ```

### 6. Initialize the Database
1. Create database tables:
   ```bash
   python -m src.db_schema
   ```
2. Populate the database with initial data:
   ```bash
   python -m scripts.populate_db
   ```

### 7. (Optional) Prepare Vector Database for RAG
```bash
python -m src.vector_db_preparation
```

### 8. (Optional) Prepare Fine-tuning Data
```bash
python -m src.finetuning_preparation
```

## Running the Application

### Option 1: Start the FastAPI Server
```bash
uvicorn src.api:app --reload
```

The API will be available at: http://127.0.0.1:8000

### Option 2: Run the Interactive Console App
```bash
python -m src.app
```

### Option 3: Test the AI Orchestration
```bash
python -m src.ai_orchestration
```

## Development Server
For development with auto-reload:
```bash
uvicorn src.api:app --reload --port 8000
```

Access the interactive API documentation at: http://127.0.0.1:8000/docs

## API Documentation

### Base URL
```
http://localhost:8000
```

### 1. Chat Endpoint
Send a message and get an AI response.

**Endpoint:** `POST /chat`

**Request:**
```json
{
  "message": "I'm feeling very anxious today",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "response": "I'm sorry to hear you're feeling anxious. Let's work through this together. Have you tried any relaxation techniques?",
  "session_id": "session_abc123",
  "metadata": {
    "sentiment": "negative",
    "next_action": "suggest_coping_strategy",
    "problem_id": "P001"
  }
}
```

### 2. Submit Feedback
Submit feedback about an AI response.

**Endpoint:** `POST /feedback`

**Request:**
```json
{
  "feedback": "This helped a little",
  "session_id": "session_abc123",
  "user_message": "I'm feeling very anxious today",
  "ai_response": "Have you tried deep breathing?",
  "problem_id": "P001",
  "suggestion_id": "S001"
}
```

**Response:**
```json
{
  "message": "Feedback received successfully",
  "feedback_id": "fb_12345",
  "sentiment": "positive",
  "next_action": "continue_same_topic"
}
```

### 3. Get Session History
Get the conversation history for a session.

**Endpoint:** `GET /sessions/{session_id}`

**Response:**
```json
{
  "session_id": "session_abc123",
  "user_id": "user_123",
  "started_at": "2025-06-09T09:30:00Z",
  "messages": [
    {
      "role": "user",
      "content": "I'm feeling very anxious today",
      "timestamp": "2025-06-09T09:30:05Z"
    },
    {
      "role": "assistant",
      "content": "I'm sorry to hear that. Have you tried deep breathing?",
      "timestamp": "2025-06-09T09:30:10Z"
    }
  ]
}
```

### 4. Get Problems
Get a list of all mental health problems.

**Endpoint:** `GET /problems`

**Response:**
```json
[
  {
    "id": "P001",
    "problem_name": "Anxiety",
    "description": "Feelings of worry, nervousness, or unease"
  },
  ...
]
```

### 5. Get Suggestions
Get suggestions, optionally filtered by problem ID.

**Endpoint:** `GET /suggestions?problem_id=P001`

**Response:**
```json
[
  {
    "suggestion_id": "S001",
    "suggestion_text": "Practice deep breathing exercises",
    "problem_id": "P001"
  },
  ...
]
```

## Utility Scripts

The `/scripts` directory contains several utility scripts for development and maintenance:

### 1. `populate_db.py`
Populates the database with initial data from the Excel file.

**Usage:**
```bash
python -m scripts.populate_db
```

### 2. `check_db.py`
Checks the database contents and provides a summary.

**Usage:**
```bash
python -m scripts.check_db
```

### 3. `inspect_data.py`
Inspects the structure of the loaded knowledge base data.

**Usage:**
```bash
python -m scripts.inspect_data
```

### 4. `inspect_feedback_prompts.py`
Inspects the feedback prompts in the database.

**Usage:**
```bash
python -m scripts.inspect_feedback_prompts
```

### 5. `update_db.py`
Drops and recreates database tables (use with caution).

**Usage:**
```bash
python -m scripts.update_db
```

## Development Roadmap

- [x] Complete implementation of database operations
- [ ] Integrate vector database for RAG capabilities
- [ ] Implement fine-tuning workflows for LLMs
- [ ] Develop a user interface for interaction
- [ ] Add authentication and user session management
- [ ] Deploy as a web service
