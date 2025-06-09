import pandas as pd
import numpy as np
from typing import List, Dict, Any
import os
import json
from .data_preprocessing import DataPreprocessor

# For demonstration purposes - in a real implementation, you would use:
# from sentence_transformers import SentenceTransformer
# from langchain.vectorstores import Chroma, FAISS
# from langchain.embeddings import HuggingFaceEmbeddings

class VectorDBPreparation:
    def __init__(self, knowledge_base: Dict[str, pd.DataFrame]):
        self.knowledge_base = knowledge_base
        # self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Example model

    def extract_text_for_embeddings(self) -> List[Dict[str, Any]]:
        """Extract text content from DataFrames for embedding generation"""
        documents = []

        # Extract from Problems
        if 'problems' in self.knowledge_base:
            for _, row in self.knowledge_base['problems'].iterrows():
                doc = {
                    'text': f"{row['problem_name']} {row.get('description', '')}",
                    'metadata': {
                        'source': 'problems',
                        'problem_id': row['problem_id'],
                        'problem_name': row['problem_name']
                    }
                }
                documents.append(doc)

        # Extract from Self Assessments
        if 'self_assessments' in self.knowledge_base:
            for _, row in self.knowledge_base['self_assessments'].iterrows():
                doc = {
                    'text': row['question_text'],
                    'metadata': {
                        'source': 'self_assessments',
                        'question_id': row['question_id'],
                        'problem_id': row['problem_id'],
                        'response_type': row['response_type']
                    }
                }
                documents.append(doc)

        # Extract from Suggestions
        if 'suggestions' in self.knowledge_base:
            for _, row in self.knowledge_base['suggestions'].iterrows():
                doc = {
                    'text': row['suggestion_text'],
                    'metadata': {
                        'source': 'suggestions',
                        'suggestion_id': row['suggestion_id'],
                        'problem_id': row['problem_id'],
                        'resource_link': row.get('resource_link', '')
                    }
                }
                documents.append(doc)

        return documents

    def generate_embeddings(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate embeddings for each document"""
        # In a real implementation, this would use the actual embedding model
        for doc in documents:
            # doc['embedding'] = self.embedding_model.encode(doc['text'])
            # For demonstration, we'll use a placeholder
            doc['embedding'] = np.random.rand(384).tolist()  # Simulating 384-dim embedding

        return documents

    def save_for_vector_db(self, documents: List[Dict[str, Any]], output_path: str):
        """Save documents with embeddings for vector database ingestion"""
        # For demonstration - in a real implementation, you would use:
        # vector_db = Chroma.from_documents(documents, embedding_function)
        # or
        # vector_db = FAISS.from_documents(documents, embedding_function)

        # Instead, we'll save to a JSON file for demonstration
        with open(output_path, 'w') as f:
            json.dump(documents, f, indent=2)

        print(f"Saved {len(documents)} documents with embeddings to {output_path}")

# Example usage
if __name__ == "__main__":
    from .data_preprocessing import DataPreprocessor
    import os

    # Load and process data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    excel_file_path = os.path.join(project_root, 'data', 'missing_values_updated.xlsx')

    preprocessor = DataPreprocessor(excel_file_path)
    knowledge_base = preprocessor.load_and_process_all_sheets()

    # Prepare vector database
    vector_prep = VectorDBPreparation(knowledge_base)
    documents = vector_prep.extract_text_for_embeddings()
    documents_with_embeddings = vector_prep.generate_embeddings(documents)

    # Save for vector database
    output_path = os.path.join(project_root, 'data', 'vector_db_documents.json')
    vector_prep.save_for_vector_db(documents_with_embeddings, output_path)