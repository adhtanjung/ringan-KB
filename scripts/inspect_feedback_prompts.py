import sys
from pathlib import Path
from sqlalchemy import create_engine, inspect

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.db_schema import FeedbackPrompt, Base

def main():
    # Setup database connection
    db_path = project_root / 'mental_health_kb.db'
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create a session
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if table exists
        inspector = inspect(engine)
        if 'feedback_prompts' not in inspector.get_table_names():
            print("Table 'feedback_prompts' does not exist.")
            return
        
        # Get all feedback prompts
        prompts = session.query(FeedbackPrompt).all()
        print(f"Found {len(prompts)} feedback prompts in the database.")
        
        # Print all feedback prompts
        for prompt in prompts:
            print(f"\nPrompt ID: {prompt.prompt_id}")
            print(f"Stage: {prompt.stage}")
            print(f"Text: {prompt.prompt_text[:100]}..." if prompt.prompt_text else "")
            print(f"Next Action: {prompt.next_action}")
        
        # Check for duplicate prompt_ids
        from collections import defaultdict
        id_counts = defaultdict(int)
        for prompt in prompts:
            id_counts[prompt.prompt_id] += 1
        
        duplicates = {k: v for k, v in id_counts.items() if v > 1}
        if duplicates:
            print("\nDuplicate prompt_ids found:", duplicates)
        else:
            print("\nNo duplicate prompt_ids found.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
