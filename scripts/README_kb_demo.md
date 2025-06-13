# Knowledge Base Usage Demonstration

This directory contains scripts that demonstrate how the mental health knowledge base is being used by the AI assistant. These scripts provide concrete evidence that the RAG (Retrieval-Augmented Generation) system is working properly and retrieving relevant information from the knowledge base.

## Available Demonstration Scripts

### 1. `kb_usage_demo.py`

This is the main demonstration script that provides comprehensive evidence of knowledge base usage. It:

- Verifies the content of the knowledge base by querying the database directly
- Shows record counts for each table in the knowledge base
- Runs test queries through the AI assistant
- Displays the retrieved source documents from the knowledge base for each query
- Provides statistics on which types of documents were retrieved

**Features:**
- Color-coded output for better readability
- Detailed metadata for each retrieved document
- Statistical breakdown of source document types

### 2. `demonstrate_kb_usage.py`

A simpler demonstration script that shows:

- Available mental health problems in the knowledge base
- Suggestions for specific problems
- Sample queries with AI responses and source documents

## How to Run

1. Make sure you have installed all required dependencies:
   ```
   pip install tabulate colorama
   ```

2. Set your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. Run the main demonstration script:
   ```
   python scripts/kb_usage_demo.py
   ```

## What to Look For

When running the demonstration scripts, pay attention to:

1. **Source Documents**: Each AI response includes references to specific documents from the knowledge base that were used to generate the response.

2. **Metadata**: Each source document includes metadata showing which table it came from (problems, suggestions, self-assessments) and its unique identifiers.

3. **Relevance**: Notice how the retrieved documents are semantically relevant to the query, showing that the vector search is working correctly.

These demonstrations provide clear evidence that the AI assistant is using the knowledge base to generate responses rather than relying solely on its pre-trained knowledge.