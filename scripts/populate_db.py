import os
import sys
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.db_schema import (
    Base, Problem, SelfAssessment, Suggestion, 
    FeedbackPrompt, NextAction, FinetuningExample, Feedback
)
from src.data_loader import DataLoader

def dataclass_to_dict_list(dataclass_list):
    """Convert a list of dataclass instances to a list of dictionaries"""
    return [
        {field.name: getattr(obj, field.name) for field in obj.__dataclass_fields__.values()}
        for obj in dataclass_list
    ]

def main():
    # Setup database connection
    db_path = project_root / 'mental_health_kb.db'
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Clear existing data in the correct order to respect foreign key constraints
        print("Clearing existing data...")
        session.query(Feedback).delete()
        session.query(FinetuningExample).delete()
        session.query(FeedbackPrompt).delete()
        session.query(SelfAssessment).delete()
        session.query(Suggestion).delete()
        session.query(NextAction).delete()
        session.query(Problem).delete()
        session.commit()
        
        # Load and process the Excel file
        print("Loading data from Excel...")
        excel_file = project_root / 'data' / 'missing_values_updated.xlsx'
        data_loader = DataLoader(excel_file)
        knowledge_base = data_loader.load_all_data()
        
        # Define the order of insertion to respect foreign key constraints
        models_to_load = [
            (Problem, knowledge_base['problems']),
            (NextAction, knowledge_base['next_actions']),
            (FeedbackPrompt, knowledge_base['feedback_prompts']),
            (SelfAssessment, knowledge_base['self_assessments']),
            (Suggestion, knowledge_base['suggestions']),
            (FinetuningExample, knowledge_base['finetuning_examples'])
        ]
        
        # Track inserted IDs to avoid duplicates
        inserted_ids = {
            'problems': set(),
            'next_actions': set(),
            'feedback_prompts': set(),
            'self_assessments': set(),
            'suggestions': set(),
            'finetuning_examples': set()
        }
        
        # Load data in the correct order
        for model_class, items in models_to_load:
            model_name = model_class.__tablename__
            if not items:
                print(f"No items to load for {model_name}")
                continue
                
            print(f"Loading {len(items)} {model_name}...")
            
            # Convert dataclass to dictionary and create model instances
            for item in items:
                try:
                    # Convert dataclass to dict
                    item_dict = {}
                    for field in item.__dataclass_fields__.values():
                        value = getattr(item, field.name)
                        # Convert any non-None values to string to avoid serialization issues
                        if value is not None:
                            item_dict[field.name] = str(value)
                        else:
                            item_dict[field.name] = None
                    
                    # Skip if we've already inserted this ID
                    id_field = next((f for f in item_dict.keys() if f.endswith('_id') or f == 'id'), None)
                    if id_field and item_dict[id_field] in inserted_ids[model_name]:
                        print(f"Skipping duplicate {model_name} with {id_field}: {item_dict[id_field]}")
                        continue
                    
                    # Create model instance and add to session
                    model_instance = model_class(**item_dict)
                    session.add(model_instance)
                    
                    # Track inserted IDs
                    if id_field:
                        inserted_ids[model_name].add(item_dict[id_field])
                    
                    # Commit after each item to catch errors early
                    session.commit()
                    
                except Exception as e:
                    session.rollback()
                    print(f"Error processing {model_name} item: {item}")
                    print(f"Error details: {e}")
                    # Continue with the next item instead of failing completely
                    continue
        
        # Commit all changes
        session.commit()
        print("Database populated successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"Error populating database: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()
