#!/usr/bin/env python3

import os
import sys
import json
from pathlib import Path
from pprint import pprint

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import the AI orchestrator
from src.ai_orchestration import MentalHealthAIOrchestrator

def main():
    print("\n=== Mental Health Knowledge Base Usage Demonstration ===")
    print("This script demonstrates how the knowledge base is being used by the AI assistant.")
    
    # Initialize the AI orchestrator with configuration
    config = {
        "db_connection_string": f"sqlite:///{project_root / 'mental_health_kb.db'}",
        "model_name": "gpt-3.5-turbo",  # Use a default model if the fine-tuned one isn't available
        "vector_db_path": str(project_root / 'data' / 'vector_db')
    }
    
    try:
        print("\nInitializing AI Orchestrator...")
        ai = MentalHealthAIOrchestrator(config)
        
        # 1. First, show available problems from the knowledge base
        print("\n1. Available Mental Health Problems in Knowledge Base:")
        problems = ai.get_problem_list()
        for i, problem in enumerate(problems):
            print(f"   {i+1}. {problem['name']} (ID: {problem['id']})")
        
        # 2. Show suggestions for a specific problem
        if problems:
            problem_id = problems[0]['id']  # Use the first problem as an example
            problem_name = problems[0]['name']
            print(f"\n2. Suggestions for '{problem_name}' from Knowledge Base:")
            suggestions = ai.get_suggestions(problem_id)
            for i, suggestion in enumerate(suggestions[:3]):  # Show first 3 suggestions
                print(f"   {i+1}. {suggestion['text'][:100]}...")
                if suggestion.get('resource'):
                    print(f"      Resource: {suggestion['resource']}")
        
        # 3. Demonstrate RAG in action with sample queries
        print("\n3. Demonstrating RAG (Retrieval-Augmented Generation):")
        
        test_queries = [
            "What are some strategies for managing anxiety?",
            "How can I help someone who is experiencing depression?",
            "What are the signs of burnout?"
        ]
        
        for i, query in enumerate(test_queries):
            print(f"\nQuery {i+1}: {query}")
            print("\nProcessing...")
            
            # Process the query
            response = ai.process_user_message(user_id="demo_user", message=query)
            
            # Display the AI response
            print("\nAI Response:")
            print(f"{response['text']}")
            
            # Display source documents (evidence of knowledge base usage)
            print("\nSource Documents (Knowledge Base References):")
            if response.get('source_documents'):
                for j, doc in enumerate(response['source_documents']):
                    print(f"\nSource {j+1}:")
                    print(f"Content: {doc['content'][:150]}...")
                    print(f"Metadata: {doc['metadata']}")
            else:
                print("No specific source documents were retrieved for this query.")
            
            print("\n" + "-"*50)
        
        print("\nDemonstration complete! The above results show how the AI assistant")
        print("retrieves and uses information from the knowledge base to generate responses.")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()