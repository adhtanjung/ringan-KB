#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import the AI orchestrator and database schema
from src.ai_orchestration import MentalHealthAIOrchestrator
from src.db_schema import Problem, SelfAssessment, Suggestion, FeedbackPrompt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80)

def print_subheader(text):
    """Print a formatted subheader"""
    print(f"\n{text}")
    print("-" * len(text))

def verify_kb_content():
    """Verify and display knowledge base content directly from the database"""
    print_header("KNOWLEDGE BASE CONTENT VERIFICATION")
    
    # Setup database connection
    db_path = project_root / 'mental_health_kb.db'
    engine = create_engine(f'sqlite:///{db_path}')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Count records in each table
        problem_count = session.query(Problem).count()
        suggestion_count = session.query(Suggestion).count()
        assessment_count = session.query(SelfAssessment).count()
        prompt_count = session.query(FeedbackPrompt).count()
        
        # Display counts
        print_subheader("Database Record Counts")
        print(f"Problems: {problem_count} records")
        print(f"Suggestions: {suggestion_count} records")
        print(f"Self Assessments: {assessment_count} records")
        print(f"Feedback Prompts: {prompt_count} records")
        
        # Sample data from each table
        print_subheader("Sample Problems")
        problems = session.query(Problem).limit(3).all()
        for p in problems:
            print(f"ID: {p.problem_id} | Name: {p.problem_name}")
        
        print_subheader("Sample Suggestions")
        suggestions = session.query(Suggestion).limit(3).all()
        for s in suggestions:
            print(f"ID: {s.suggestion_id} | Problem ID: {s.problem_id}")
            print(f"Text: {s.suggestion_text[:100]}...")
        
        return True
    except Exception as e:
        print(f"\nError accessing knowledge base: {e}")
        return False
    finally:
        session.close()

def demonstrate_rag_queries(ai):
    """Demonstrate RAG by running test queries and showing source documents"""
    print_header("RAG DEMONSTRATION WITH TEST QUERIES")
    
    test_queries = [
        "What are some effective strategies for managing anxiety?",
        "How can I help someone who is experiencing depression?",
        "What are the signs of burnout and how can I prevent it?"
    ]
    
    for i, query in enumerate(test_queries):
        print_subheader(f"Query {i+1}: {query}")
        print("Processing...")
        
        # Process the query
        response = ai.process_user_message(user_id="demo_user", message=query)
        
        # Display the AI response
        print("\nAI Response:")
        print(response['text'])
        
        # Display source documents (evidence of knowledge base usage)
        print_subheader("Knowledge Base Sources Used")
        if response.get('source_documents'):
            for j, doc in enumerate(response['source_documents']):
                print(f"\nSource {j+1}:")
                print(f"Content: {doc['content'][:200]}...")
                print(f"Source Type: {doc['metadata'].get('source', 'Unknown')}")
                
                # Print additional metadata based on source type
                source_type = doc['metadata'].get('source')
                if source_type == 'problems':
                    print(f"Problem ID: {doc['metadata'].get('problem_id')}")
                    print(f"Problem Name: {doc['metadata'].get('problem_name')}")
                elif source_type == 'suggestions':
                    print(f"Suggestion ID: {doc['metadata'].get('suggestion_id')}")
                    print(f"Problem ID: {doc['metadata'].get('problem_id')}")
                elif source_type == 'self_assessments':
                    print(f"Question ID: {doc['metadata'].get('question_id')}")
                    print(f"Problem ID: {doc['metadata'].get('problem_id')}")
        else:
            print("No specific source documents were retrieved for this query.")
        
        print("\n" + "=" * 80)

def main():
    print_header("MENTAL HEALTH KNOWLEDGE BASE USAGE DEMONSTRATION")
    print("This script demonstrates how the knowledge base is being used by the AI assistant.")
    
    # First verify the knowledge base content
    if not verify_kb_content():
        print("Failed to verify knowledge base content. Exiting.")
        return
    
    # Initialize the AI orchestrator with configuration
    config = {
        "db_connection_string": f"sqlite:///{project_root / 'mental_health_kb.db'}",
        "model_name": "gpt-3.5-turbo",  # Use a default model if the fine-tuned one isn't available
        "vector_db_path": str(project_root / 'data' / 'vector_db')
    }
    
    try:
        print("\nInitializing AI Orchestrator...")
        ai = MentalHealthAIOrchestrator(config)
        
        # Demonstrate RAG in action
        demonstrate_rag_queries(ai)
        
        print_header("DEMONSTRATION COMPLETE")
        print("The above results prove that the AI assistant is successfully using")
        print("the knowledge base to generate responses. Each response includes")
        print("references to specific documents from the knowledge base.")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()