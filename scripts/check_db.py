import sys
from pathlib import Path
from sqlalchemy import create_engine, inspect, text

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.db_schema import Base, Problem, SelfAssessment, Suggestion, FeedbackPrompt, NextAction, FinetuningExample, Feedback

def main():
    # Setup database connection
    db_path = project_root / 'mental_health_kb.db'
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create a session
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Get table names
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        
        print("\n=== Database Summary ===")
        for table_name in table_names:
            # Count rows in each table
            count = session.execute(text(f'SELECT COUNT(*) FROM {table_name}')).scalar()
            print(f"{table_name}: {count} rows")
        
        # Print some sample data
        print("\n=== Sample Data ===")
        
        # Sample problems
        print("\nSample Problems:")
        problems = session.query(Problem).limit(3).all()
        for p in problems:
            print(f"{p.problem_id}: {p.problem_name}")
        
        # Sample suggestions
        print("\nSample Suggestions:")
        suggestions = session.query(Suggestion).limit(3).all()
        for s in suggestions:
            print(f"{s.suggestion_id}: {s.suggestion_text[:100]}...")
        
        # Sample feedback prompts
        print("\nFeedback Prompts:")
        prompts = session.query(FeedbackPrompt).all()
        for p in prompts:
            print(f"{p.prompt_id} ({p.stage}): {p.prompt_text[:100]}...")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
