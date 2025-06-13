#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import json
import webbrowser
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import the AI orchestrator and database schema
from src.ai_orchestration import MentalHealthAIOrchestrator
from src.db_schema import Problem, SelfAssessment, Suggestion, FeedbackPrompt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

def get_kb_statistics():
    """Get statistics about the knowledge base"""
    # Setup database connection
    db_path = project_root / 'mental_health_kb.db'
    engine = create_engine(f'sqlite:///{db_path}')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Count records in each table
        stats = {
            'problems': session.query(Problem).count(),
            'suggestions': session.query(Suggestion).count(),
            'self_assessments': session.query(SelfAssessment).count(),
            'feedback_prompts': session.query(FeedbackPrompt).count()
        }
        return stats
    except Exception as e:
        print(f"Error accessing knowledge base: {e}")
        return {'problems': 0, 'suggestions': 0, 'self_assessments': 0, 'feedback_prompts': 0}
    finally:
        session.close()

def run_test_queries(ai):
    """Run test queries and collect results"""
    test_queries = [
        "What are some effective strategies for managing anxiety?",
        "How can I help someone who is experiencing depression?",
        "What are the signs of burnout and how can I prevent it?",
        "What self-care practices are recommended for mental health?"
    ]
    
    results = []
    for query in test_queries:
        print(f"Processing query: {query}")
        response = ai.process_user_message(user_id="demo_user", message=query)
        
        results.append({
            'query': query,
            'response': response['text'],
            'source_documents': response.get('source_documents', [])
        })
    
    return results

def main():
    print("Generating Knowledge Base Usage Report...")
    
    # Get knowledge base statistics
    kb_stats = get_kb_statistics()
    
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
        query_results = run_test_queries(ai)
        
        # Generate HTML report
        print("Generating HTML report...")
        html_report = generate_html_report(kb_stats, query_results)
        
        # Save the report
        report_path = project_root / 'scripts' / 'kb_usage_report.html'
        with open(report_path, 'w') as f:
            f.write(html_report)
        
        print(f"Report generated and saved to {report_path}")
        print("Opening report in browser...")
        
        # Open the report in the default browser
        webbrowser.open(f'file://{report_path}')
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()