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

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Ensure the Excel file is placed in the data/ directory
5. Run the application:
   ```
   python -m src.app
   ```

## Usage

Currently, the application loads and displays the knowledge base data from the Excel file. Future implementations will include:

1. Data Preparation :

   ```
   python -m src.data_preprocessing
   ```

2. Database Setup :

   ```
   python -m src.db_schema
   ```

3. Vector Database Preparation :

   ```
   python -m src.vector_db_preparation
   ```

4. Fine-tuning Data Preparation :

   ```
   python -m src.finetuning_preparation
   ```

5. AI Orchestration :

   ```
   python -m src.ai_orchestration
   ```

## Development Roadmap

- Complete implementation of database operations
- Integrate vector database for RAG capabilities
- Implement fine-tuning workflows for LLMs
- Develop a user interface for interaction
- Add authentication and user session management
- Deploy as a web service
