import pandas as pd
import numpy as np
from typing import List, Dict, Any
import os
import json
from .data_preprocessing import DataPreprocessor
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class VectorDBPreparation:
    def __init__(self, knowledge_base: Dict[str, pd.DataFrame]):
        self.knowledge_base = knowledge_base
        # self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Example model

    def extract_text_for_embeddings(self) -> List[Dict[str, Any]]:
        """Extract and combine text content from DataFrames for embedding generation."""
        documents = []
        problems_df = self.knowledge_base.get('problems')
        assessments_df = self.knowledge_base.get('self_assessments')
        suggestions_df = self.knowledge_base.get('suggestions')

        if problems_df is not None:
            for _, problem_row in problems_df.iterrows():
                problem_id = problem_row['problem_id']
                problem_name = problem_row['problem_name']
                description = problem_row.get('description', '')

                combined_text = f"Problem: {problem_name}\nDescription: {description}\n"

                # Add related self-assessment questions
                if assessments_df is not None:
                    related_assessments = assessments_df[assessments_df['problem_id'] == problem_id]
                    if not related_assessments.empty:
                        combined_text += "\nSelf-Assessment Questions:\n"
                        for _, assess_row in related_assessments.iterrows():
                            combined_text += f"- {assess_row['question_text']}\n"

                # Add related suggestions
                if suggestions_df is not None:
                    related_suggestions = suggestions_df[suggestions_df['problem_id'] == problem_id]
                    if not related_suggestions.empty:
                        combined_text += "\nSuggestions & Coping Strategies:\n"
                        for _, sugg_row in related_suggestions.iterrows():
                            combined_text += f"- {sugg_row['suggestion_text']}\n"
                            if sugg_row.get('resource_link'):
                                combined_text += f"  (Resource: {sugg_row['resource_link']})\n"
                
                doc = {
                    'text': combined_text.strip(),
                    'metadata': {
                        'source': 'combined_problem_info',
                        'problem_id': problem_id,
                        'problem_name': problem_name
                    }
                }
                documents.append(doc)
        
        # Fallback: if no problems, add individual assessments and suggestions as before
        # This ensures that if the 'problems' sheet is missing, other data can still be indexed.
        if not documents:
            if assessments_df is not None:
                for _, row in assessments_df.iterrows():
                    documents.append({
                        'text': row['question_text'],
                        'metadata': {
                            'source': 'self_assessments',
                            'question_id': row['question_id'],
                            'problem_id': row['problem_id'],
                            'response_type': row['response_type']
                        }
                    })
            if suggestions_df is not None:
                for _, row in suggestions_df.iterrows():
                    documents.append({
                        'text': row['suggestion_text'],
                        'metadata': {
                            'source': 'suggestions',
                            'suggestion_id': row['suggestion_id'],
                            'problem_id': row['problem_id'],
                            'resource_link': row.get('resource_link', '')
                        }
                    })

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
        """Save documents with embeddings to a proper vector database"""
        # Initialize HuggingFace embeddings
        embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        
        # Extract texts and metadatas
        texts = [doc['text'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        
        # Create and persist Chroma vector store
        vectordb = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas,
            persist_directory=output_path
        )
        vectordb.persist()

def main():
    """Main function to prepare the vector database"""
    # Load the knowledge base data
    data_preprocessor = DataPreprocessor('data/missing_values_updated.xlsx')
    knowledge_base = data_preprocessor.load_and_process_all_sheets()
    
    # Initialize vector DB preparation
    vector_db_prep = VectorDBPreparation(knowledge_base)
    
    # Extract text content
    documents = vector_db_prep.extract_text_for_embeddings()
    
    # Save to vector database
    vector_db_path = os.path.join('data', 'vector_db')
    vector_db_prep.save_for_vector_db(documents, vector_db_path)
    
if __name__ == '__main__':
    main()