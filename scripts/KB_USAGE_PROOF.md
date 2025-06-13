# Knowledge Base Usage Proof

This document provides evidence that the mental health knowledge base is being actively used by the AI assistant system. The demonstration scripts in this directory show how the RAG (Retrieval-Augmented Generation) system retrieves relevant information from the knowledge base when responding to user queries.

## Evidence of Knowledge Base Usage

### 1. Database Content Verification

The demonstration scripts verify that the knowledge base contains structured data across multiple tables:
- Problems
- Suggestions
- Self-Assessments
- Feedback Prompts

This data is stored in the SQLite database (`mental_health_kb.db`) and is accessible through the ORM models defined in `src/db_schema.py`.

### 2. Vector Database Integration

The system uses a vector database (ChromaDB) to store embeddings of the knowledge base content, enabling semantic search. The `vector_db_preparation.py` script shows how text from the knowledge base is processed and stored in the vector database.

### 3. RAG System in Action

The demonstration scripts show the RAG system in action by:
1. Sending test queries to the AI assistant
2. Retrieving relevant documents from the knowledge base
3. Using these documents to generate informed responses
4. Displaying the source documents with their metadata

### 4. Source Document Traceability

Each response from the AI assistant includes source documents with metadata that traces back to the original knowledge base entries. This metadata includes:
- Source type (problems, suggestions, self-assessments)
- Unique identifiers (problem_id, suggestion_id, etc.)
- Original content

## Available Demonstration Scripts

1. **`simple_kb_demo.py`**: A straightforward demonstration that shows database content and runs test queries with source document retrieval.

2. **`demonstrate_kb_usage.py`**: Shows available mental health problems, suggestions, and runs sample queries with source document retrieval.

3. **`kb_usage_demo.py`**: A more comprehensive demonstration with formatted output (requires tabulate and colorama).

4. **`kb_usage_report.py`**: Generates an HTML report with visual evidence of knowledge base usage, including statistics and query results with source documents.

## How to Run the Demonstrations

1. Simple demonstration:
   ```
   python scripts/simple_kb_demo.py
   ```

2. Generate HTML report:
   ```
   python scripts/kb_usage_report.py
   ```
   This will generate an HTML report and open it in your default browser.

## Conclusion

These demonstrations provide clear evidence that the AI assistant is using the knowledge base to generate responses rather than relying solely on its pre-trained knowledge. The source documents retrieved for each query show that the system is successfully retrieving relevant information from the knowledge base based on semantic similarity.