#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.data_loader import DataLoader
from src.vector_db_preparation import VectorDBPreparation
from src.models import Problem, SelfAssessment, Suggestion, FeedbackPrompt, NextAction, FinetuningExample
import pandas as pd

class CustomDataLoader(DataLoader):
    def load_problems(self) -> list:
        return self._load_sheet('Problems', Problem)

    def load_self_assessments(self) -> list:
        return self._load_sheet('SelfAssessment', SelfAssessment)

    def load_suggestions(self) -> list:
        return self._load_sheet('Suggestions', Suggestion)

    def load_feedback_prompts(self) -> list:
        return self._load_sheet('FeedbackPrompts', FeedbackPrompt)

    def load_next_actions(self) -> list:
        return self._load_sheet('NextActions', NextAction)

    def load_finetuning_examples(self) -> list:
        return self._load_sheet('FinetuningExamples', FinetuningExample)

def main():
    # Path to the expanded knowledge base Excel file
    expanded_kb_path = project_root / 'data' / 'expanded_mental_health_kb_data.xlsx'
    
    if not expanded_kb_path.exists():
        print(f"Error: Expanded knowledge base file not found at {expanded_kb_path}")
        print("Please run 'python3 src/expanded_data_model.py' first to generate the file.")
        sys.exit(1)
    
    print(f"Loading expanded knowledge base from {expanded_kb_path}...")
    
    # Load the data using CustomDataLoader
    try:
        data_loader = CustomDataLoader(expanded_kb_path)
        knowledge_base = data_loader.load_all_data()
        print("Successfully loaded expanded knowledge base data.")
        
        # Convert to DataFrames for vector DB preparation
        kb_dataframes = {}
        for key, items in knowledge_base.items():
            if items:
                # Convert dataclass objects to dictionaries
                records = []
                for item in items:
                    item_dict = {}
                    for field in item.__dataclass_fields__.values():
                        item_dict[field.name] = getattr(item, field.name)
                    records.append(item_dict)
                kb_dataframes[key] = pd.DataFrame(records)
        
        # Prepare vector database
        print("Preparing vector database...")
        vector_db_path = project_root / 'data' / 'vector_db'
        vector_db_prep = VectorDBPreparation(kb_dataframes)
        documents = vector_db_prep.extract_text_for_embeddings()
        
        # Save to vector database
        print(f"Saving {len(documents)} documents to vector database...")
        vector_db_prep.save_for_vector_db(documents, str(vector_db_path))
        
        print("\nExpanded knowledge base has been successfully integrated into the project.")
        print("The vector database has been updated with the expanded mental health information.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()