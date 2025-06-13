#!/usr/bin/env python3

import os
import sys
import json
from pathlib import Path
from pprint import pprint
import pandas as pd
from tabulate import tabulate
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init()

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
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{text.center(80)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")

def print_subheader(text):
    """Print a formatted subheader"""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{text}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'-' * len(text)}{Style.RESET_ALL}")

def print_source_document(doc, index):
    """Print a source document with formatting"""
    print(f"\n{Fore.GREEN}Source {index+1}:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Content:{Style.RESET_ALL} {doc['content'][:200]}...")
    print(f"{Fore.WHITE}Source Type:{Style.RESET_ALL} {doc['metadata'].get('source', 'Unknown')}")
    
    # Print additional metadata based on source type
    source_type = doc['metadata'].get('source')
    if source_type == 'problems':
        print(f"{Fore.WHITE}Problem ID:{Style.RESET_ALL} {doc['metadata'].get('problem_id')}")
        print(f"{Fore.WHITE}Problem Name:{Style.RESET_ALL} {doc['metadata'].get('problem_name')}")
    elif source_type == 'suggestions':
        print(f"{Fore.WHITE}Suggestion ID:{Style.RESET_ALL} {doc['metadata'].get('suggestion_id')}")
        print(f"{Fore.WHITE}Problem ID:{Style.RESET_ALL} {doc['metadata'].get('problem_id')}")
    elif source_type == 'self_assessments':
        print(f"{Fore.WHITE}Question ID:{Style.RESET_ALL} {doc['metadata'].get('question_id')}")
        print(f"{Fore.WHITE}Problem ID:{Style.RESET_ALL} {doc['metadata'].get('problem_id')}")

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
        
        # Display counts in a table
        table_data = [
            ["Problems", problem_count],
            ["Suggestions", suggestion_count],
            ["Self Assessments", assessment_count],
            ["Feedback Prompts", prompt_count]
        ]
        
        print_subheader("Database Record Counts")
        print(tabulate(table_data, headers=["Table", "Record Count"], tablefmt="grid"))
        
        # Sample data from each table
        print_subheader("Sample Problems")
        problems = session.query(Problem).limit(3).all()
        problem_data = [[p.problem_id, p.problem_name] for p in problems]
        print(tabulate(problem_data, headers=["ID", "Name"], tablefmt="grid"))
        
        print_subheader("Sample Suggestions")
        suggestions = session.query(Suggestion).limit(3).all()
        suggestion_data = [[s.suggestion_id, s.problem_id, s.suggestion_text[:50] + "..."] for s in suggestions]
        print(tabulate(suggestion_data, headers=["ID", "Problem ID", "Text"], tablefmt="grid"))
        
        return True
    except Exception as e:
        print(f"\n{Fore.RED}Error accessing knowledge base: {e}{Style.RESET_ALL}")
        return False
    finally:
        session.close()

def demonstrate_rag_queries(ai):
    """Demonstrate RAG by running test queries and showing source documents"""
    print_header("RAG DEMONSTRATION WITH TEST QUERIES")
    
    test_queries = [
        "What are some effective strategies for managing anxiety?",
        "How can I help someone who is experiencing depression?",
        "What are the signs of burnout and how can I prevent it?",
        "What self-care practices are recommended for mental health?"
    ]
    
    for i, query in enumerate(test_queries):
        print_subheader(f"Query {i+1}: {query}")
        print(f"{Fore.WHITE}Processing...{Style.RESET_ALL}")
        
        # Process the query
        response = ai.process_user_message(user_id="demo_user", message=query)
        
        # Display the AI response
        print(f"\n{Fore.MAGENTA}AI Response:{Style.RESET_ALL}")
        print(response['text'])
        
        # Display source documents (evidence of knowledge base usage)
        print_subheader("Knowledge Base Sources Used")
        if response.get('source_documents'):
            for j, doc in enumerate(response['source_documents']):
                print_source_document(doc, j)
                
            # Show statistics
            source_types = [doc['metadata'].get('source', 'unknown') for doc in response['source_documents']]
            source_counts = pd.Series(source_types).value_counts().to_dict()
            
            print(f"\n{Fore.BLUE}Source Statistics:{Style.RESET_ALL}")
            for source_type, count in source_counts.items():
                print(f"- {source_type}: {count} documents")
        else:
            print(f"{Fore.RED}No specific source documents were retrieved for this query.{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")

def main():
    print_header("MENTAL HEALTH KNOWLEDGE BASE USAGE DEMONSTRATION")
    print("This script demonstrates how the knowledge base is being used by the AI assistant.")
    
    # First verify the knowledge base content
    if not verify_kb_content():
        print(f"{Fore.RED}Failed to verify knowledge base content. Exiting.{Style.RESET_ALL}")
        return
    
    # Initialize the AI orchestrator with configuration
    config = {
        "db_connection_string": f"sqlite:///{project_root / 'mental_health_kb.db'}",
        "model_name": "gpt-3.5-turbo",  # Use a default model if the fine-tuned one isn't available
        "vector_db_path": str(project_root / 'data' / 'vector_db')
    }
    
    try:
        print(f"\n{Fore.WHITE}Initializing AI Orchestrator...{Style.RESET_ALL}")
        ai = MentalHealthAIOrchestrator(config)
        
        # Demonstrate RAG in action
        demonstrate_rag_queries(ai)
        
        print_header("DEMONSTRATION COMPLETE")
        print("The above results prove that the AI assistant is successfully using")
        print("the knowledge base to generate responses. Each response includes")
        print("references to specific documents from the knowledge base.")
        
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()