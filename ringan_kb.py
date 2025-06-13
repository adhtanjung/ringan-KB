#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path
import webbrowser
from datetime import datetime
import json
import pandas as pd
from tabulate import tabulate
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init()

# Add the project root to the Python path
project_root = Path(__file__).parent
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
        
        stats = {
            'problems': problem_count,
            'suggestions': suggestion_count,
            'self_assessments': assessment_count,
            'feedback_prompts': prompt_count
        }
        
        return stats
    except Exception as e:
        print(f"\n{Fore.RED}Error accessing knowledge base: {e}{Style.RESET_ALL}")
        return {'problems': 0, 'suggestions': 0, 'self_assessments': 0, 'feedback_prompts': 0}
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
    
    results = []
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
        
        # Store results for report generation
        results.append({
            'query': query,
            'response': response['text'],
            'source_documents': response.get('source_documents', [])
        })
    
    return results

def generate_html_report(kb_stats, query_results):
    """Generate an HTML report showing knowledge base usage"""
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Knowledge Base Usage Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; color: #333; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            h1 {{ color: #2c3e50; text-align: center; margin-bottom: 30px; }}
            h2 {{ color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 40px; }}
            h3 {{ color: #2980b9; }}
            .stats-container {{ display: flex; justify-content: space-around; flex-wrap: wrap; margin: 20px 0; }}
            .stat-box {{ background-color: #f8f9fa; border-radius: 8px; padding: 20px; margin: 10px; min-width: 200px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .stat-box h3 {{ margin-top: 0; color: #2c3e50; }}
            .stat-box p {{ font-size: 24px; font-weight: bold; color: #3498db; margin: 10px 0; }}
            .query-section {{ background-color: #f8f9fa; border-radius: 8px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .query {{ font-weight: bold; color: #2c3e50; font-size: 18px; background-color: #e8f4fc; padding: 10px; border-radius: 5px; }}
            .response {{ background-color: #fff; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #3498db; }}
            .source-document {{ background-color: #f0f7fb; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #27ae60; }}
            .metadata {{ font-size: 14px; color: #7f8c8d; margin-top: 10px; }}
            .metadata span {{ font-weight: bold; color: #2c3e50; }}
            .timestamp {{ text-align: center; margin-top: 40px; color: #7f8c8d; font-size: 14px; }}
            .no-sources {{ color: #e74c3c; font-style: italic; }}
            .highlight {{ background-color: #ffffcc; padding: 2px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Mental Health Knowledge Base Usage Report</h1>
            
            <h2>Knowledge Base Statistics</h2>
            <div class="stats-container">
                <div class="stat-box">
                    <h3>Problems</h3>
                    <p>{kb_stats['problems']}</p>
                    <span>Records</span>
                </div>
                <div class="stat-box">
                    <h3>Suggestions</h3>
                    <p>{kb_stats['suggestions']}</p>
                    <span>Records</span>
                </div>
                <div class="stat-box">
                    <h3>Self Assessments</h3>
                    <p>{kb_stats['self_assessments']}</p>
                    <span>Records</span>
                </div>
                <div class="stat-box">
                    <h3>Feedback Prompts</h3>
                    <p>{kb_stats['feedback_prompts']}</p>
                    <span>Records</span>
                </div>
            </div>
            
            <h2>RAG System Demonstration</h2>
            <p>The following examples demonstrate how the AI assistant uses the knowledge base to answer queries. 
            Each response includes source documents retrieved from the knowledge base that were used to generate the answer.</p>
    """
    
    # Add each query and response
    for i, result in enumerate(query_results):
        html += f"""
            <div class="query-section">
                <div class="query">Query {i+1}: {result['query']}</div>
                <div class="response">{result['response']}</div>
                <h3>Source Documents Used</h3>
        """
        
        if result['source_documents']:
            for j, doc in enumerate(result['source_documents']):
                source_type = doc['metadata'].get('source', 'Unknown')
                source_id = ""
                if source_type == 'problems':
                    source_id = f"Problem ID: {doc['metadata'].get('problem_id')}"
                elif source_type == 'suggestions':
                    source_id = f"Suggestion ID: {doc['metadata'].get('suggestion_id')}"
                elif source_type == 'self_assessments':
                    source_id = f"Question ID: {doc['metadata'].get('question_id')}"
                
                html += f"""
                <div class="source-document">
                    <h4>Source {j+1}</h4>
                    <p>{doc['content'][:300]}...</p>
                    <div class="metadata">
                        <span>Source Type:</span> {source_type}<br>
                        <span>{source_id}</span>
                    </div>
                </div>
                """
        else:
            html += "<p class='no-sources'>No specific source documents were retrieved for this query.</p>"
        
        html += "</div>"
    
    # Close the HTML
    html += f"""
            <div class="timestamp">Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
    </body>
    </html>
    """
    
    return html

def run_api_server():
    """Run the FastAPI server"""
    print_header("STARTING API SERVER")
    print("Starting the FastAPI server...")
    
    try:
        import uvicorn
        from src.api import app
        from src.db_schema import init_db
        
        print(f"{Fore.GREEN}API server will be available at: http://127.0.0.1:8000{Style.RESET_ALL}")
        print(f"{Fore.GREEN}API documentation will be available at: http://127.0.0.1:8000/docs{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Press Ctrl+C to stop the server{Style.RESET_ALL}")
        
        # Initialize database
        init_db('sqlite:///mental_health_kb.db')
        
        # Run the server
        uvicorn.run("src.api:app", host="127.0.0.1", port=8000, reload=True)
    except ImportError:
        print(f"{Fore.RED}Error: uvicorn or FastAPI not installed. Please install with 'pip install uvicorn fastapi'{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error starting API server: {e}{Style.RESET_ALL}")

def run_frontend_server():
    """Run a simple HTTP server for the frontend"""
    print_header("STARTING FRONTEND SERVER")
    
    frontend_dir = project_root / 'frontend'
    if not frontend_dir.exists():
        print(f"{Fore.RED}Error: Frontend directory not found at {frontend_dir}{Style.RESET_ALL}")
        return
    
    try:
        import http.server
        import socketserver
        
        # Change to the frontend directory
        os.chdir(frontend_dir)
        
        # Set up the server
        PORT = 8080
        Handler = http.server.SimpleHTTPRequestHandler
        
        print(f"{Fore.GREEN}Frontend server will be available at: http://localhost:{PORT}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Press Ctrl+C to stop the server{Style.RESET_ALL}")
        
        # Start the server
        with socketserver.TCPServer(("localhost", PORT), Handler) as httpd:
            print(f"Serving at http://localhost:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"{Fore.RED}Error starting frontend server: {e}{Style.RESET_ALL}")

def setup_database():
    """Set up the database with initial data"""
    print_header("DATABASE SETUP")
    
    try:
        # Check if the database exists
        db_path = project_root / 'mental_health_kb.db'
        
        if db_path.exists():
            print(f"{Fore.YELLOW}Database already exists at {db_path}{Style.RESET_ALL}")
            choice = input("Do you want to recreate the database? (y/n): ").lower()
            if choice != 'y':
                print("Skipping database creation.")
                return
            else:
                # Delete the existing database
                db_path.unlink()
                print(f"{Fore.GREEN}Deleted existing database.{Style.RESET_ALL}")
        
        # Create database tables
        print("Creating database tables...")
        from src.db_schema import Base, engine
        Base.metadata.create_all(engine)
        print(f"{Fore.GREEN}Database tables created successfully.{Style.RESET_ALL}")
        
        # Populate the database with initial data
        print("Populating database with initial data...")
        from scripts.populate_db import main as populate_db_main
        populate_db_main()
        print(f"{Fore.GREEN}Database populated successfully.{Style.RESET_ALL}")
        
        # Prepare vector database for RAG
        print("Preparing vector database for RAG...")
        from src.vector_db_preparation import main as vector_db_main
        vector_db_main()
        print(f"{Fore.GREEN}Vector database prepared successfully.{Style.RESET_ALL}")
        
        return True
    except Exception as e:
        print(f"{Fore.RED}Error setting up database: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False

def interactive_chat():
    """Run an interactive chat session with the AI assistant"""
    print_header("INTERACTIVE CHAT SESSION")
    
    # Initialize the AI orchestrator
    config = {
        "db_connection_string": f"sqlite:///{project_root / 'mental_health_kb.db'}",
        "model_name": "gpt-3.5-turbo",
        "vector_db_path": str(project_root / 'data' / 'vector_db')
    }
    
    try:
        print("Initializing AI Orchestrator...")
        ai = MentalHealthAIOrchestrator(config)
        
        print(f"\n{Fore.GREEN}AI Assistant initialized. You can start chatting!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Type 'exit', 'quit', or 'q' to end the session.{Style.RESET_ALL}\n")
        
        session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        while True:
            user_input = input(f"{Fore.CYAN}You: {Style.RESET_ALL}")
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print(f"\n{Fore.GREEN}Chat session ended.{Style.RESET_ALL}")
                break
            
            # Process the user message
            response = ai.process_user_message(user_id=session_id, message=user_input)
            
            # Display the AI response
            print(f"\n{Fore.MAGENTA}AI: {Style.RESET_ALL}{response['text']}\n")
            
            # Optionally show source documents
            if response.get('source_documents'):
                show_sources = input("Would you like to see the knowledge base sources used? (y/n): ").lower()
                if show_sources == 'y':
                    print_subheader("Knowledge Base Sources Used")
                    for j, doc in enumerate(response['source_documents']):
                        print_source_document(doc, j)
    
    except Exception as e:
        print(f"\n{Fore.RED}Error in chat session: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

def generate_report():
    """Generate a knowledge base usage report"""
    print_header("GENERATING KNOWLEDGE BASE USAGE REPORT")
    
    # Get knowledge base statistics
    kb_stats = verify_kb_content()
    
    # Initialize the AI orchestrator
    config = {
        "db_connection_string": f"sqlite:///{project_root / 'mental_health_kb.db'}",
        "model_name": "gpt-3.5-turbo",
        "vector_db_path": str(project_root / 'data' / 'vector_db')
    }
    
    try:
        # Initialize AI orchestrator
        print("Initializing AI Orchestrator...")
        ai = MentalHealthAIOrchestrator(config)
        
        # Run test queries
        print("Running test queries...")
        query_results = demonstrate_rag_queries(ai)
        
        # Generate HTML report
        print("Generating HTML report...")
        html_report = generate_html_report(kb_stats, query_results)
        
        # Save the report
        report_path = project_root / 'reports' / 'kb_usage_report.html'
        report_path.parent.mkdir(exist_ok=True)  # Create reports directory if it doesn't exist
        with open(report_path, 'w') as f:
            f.write(html_report)
        
        print(f"\n{Fore.GREEN}Report generated and saved to {report_path}{Style.RESET_ALL}")
        print("Opening report in browser...")
        
        # Open the report in the default browser
        webbrowser.open(f'file://{report_path}')
        
    except Exception as e:
        print(f"\n{Fore.RED}Error generating report: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description="Ringan Mental Health Knowledge Base Toolkit")
    parser.add_argument('--setup', action='store_true', help='Set up the database and vector store')
    parser.add_argument('--verify', action='store_true', help='Verify knowledge base content')
    parser.add_argument('--demo', action='store_true', help='Run a demonstration of the RAG system')
    parser.add_argument('--report', action='store_true', help='Generate a knowledge base usage report')
    parser.add_argument('--chat', action='store_true', help='Start an interactive chat session')
    parser.add_argument('--api', action='store_true', help='Start the API server')
    parser.add_argument('--frontend', action='store_true', help='Start the frontend server')
    parser.add_argument('--all', action='store_true', help='Run all components (setup, verify, demo, report)')
    
    args = parser.parse_args()
    
    print_header("RINGAN MENTAL HEALTH KNOWLEDGE BASE TOOLKIT")
    
    # If no arguments are provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        print(f"\n{Fore.YELLOW}Example usage:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}python ringan_kb.py --setup{Style.RESET_ALL}  # Set up the database and vector store")
        print(f"  {Fore.GREEN}python ringan_kb.py --verify{Style.RESET_ALL} # Verify knowledge base content")
        print(f"  {Fore.GREEN}python ringan_kb.py --demo{Style.RESET_ALL}   # Run a demonstration of the RAG system")
        print(f"  {Fore.GREEN}python ringan_kb.py --report{Style.RESET_ALL} # Generate a knowledge base usage report")
        print(f"  {Fore.GREEN}python ringan_kb.py --chat{Style.RESET_ALL}   # Start an interactive chat session")
        print(f"  {Fore.GREEN}python ringan_kb.py --api{Style.RESET_ALL}    # Start the API server")
        print(f"  {Fore.GREEN}python ringan_kb.py --frontend{Style.RESET_ALL} # Start the frontend server")
        print(f"  {Fore.GREEN}python ringan_kb.py --all{Style.RESET_ALL}    # Run all components")
        return
    
    # Run the selected components
    if args.setup or args.all:
        setup_database()
    
    if args.verify or args.all:
        verify_kb_content()
    
    if args.demo or args.all:
        # Initialize the AI orchestrator
        config = {
            "db_connection_string": f"sqlite:///{project_root / 'mental_health_kb.db'}",
            "model_name": "gpt-3.5-turbo",
            "vector_db_path": str(project_root / 'data' / 'vector_db')
        }
        
        try:
            print("Initializing AI Orchestrator...")
            ai = MentalHealthAIOrchestrator(config)
            demonstrate_rag_queries(ai)
        except Exception as e:
            print(f"\n{Fore.RED}Error in demo: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()
    
    if args.report or args.all:
        generate_report()
    
    if args.chat:
        interactive_chat()
    
    if args.api:
        run_api_server()
    
    if args.frontend:
        run_frontend_server()

if __name__ == "__main__":
    main()