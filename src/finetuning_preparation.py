import pandas as pd
import json
import os
from typing import Dict, List
from .data_preprocessing import DataPreprocessor

class FinetuningPreparation:
    def __init__(self, finetuning_examples: pd.DataFrame):
        self.finetuning_examples = finetuning_examples

    def prepare_for_openai_finetuning(self, output_path: str):
        """Prepare data for OpenAI fine-tuning format"""
        formatted_examples = []

        for _, row in self.finetuning_examples.iterrows():
            # Define the base system message with explicit language instruction
            system_content = "You are a mental health assistant trained to provide empathetic and helpful guidance. Respond exclusively in English."

            # Add problem context if available
            if pd.notna(row.get('problem')):
                system_content += f" The current topic is related to {row['problem']}."

            # Format according to OpenAI's fine-tuning format
            example = {
                "messages": [
                    {"role": "system", "content": system_content}, # System message updated here
                    {"role": "user", "content": row['prompt']},
                    {"role": "assistant", "content": row['completion']}
                ]
            }

            # Add conversation context if available
            if pd.notna(row.get('conversation_id')):
                example["conversation_id"] = row['conversation_id']

            formatted_examples.append(example)

        # Save to JSONL format (one JSON object per line)
        with open(output_path, 'w') as f:
            for example in formatted_examples:
                f.write(json.dumps(example) + '\n')

        print(f"Saved {len(formatted_examples)} fine-tuning examples to {output_path}")

    def prepare_for_huggingface_finetuning(self, output_path: str):
        """Prepare data for Hugging Face fine-tuning format"""
        formatted_examples = []

        for _, row in self.finetuning_examples.iterrows():
            # Format for instruction fine-tuning
            example = {
                "instruction": row['prompt'],
                "output": row['completion']
            }

            # Add problem context if available
            if pd.notna(row.get('problem')):
                example["context"] = f"Topic: {row['problem']}"

            # Add conversation context if available
            if pd.notna(row.get('conversation_id')):
                example["conversation_id"] = row['conversation_id']

            formatted_examples.append(example)

        # Save to JSON format
        with open(output_path, 'w') as f:
            json.dump(formatted_examples, f, indent=2)

        print(f"Saved {len(formatted_examples)} fine-tuning examples to {output_path}")

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

    # Prepare fine-tuning data
    finetuning_prep = FinetuningPreparation(knowledge_base['finetuning_examples'])

    # Save for OpenAI fine-tuning
    openai_output_path = os.path.join(project_root, 'data', 'openai_finetuning.jsonl')
    finetuning_prep.prepare_for_openai_finetuning(openai_output_path)

    # Save for Hugging Face fine-tuning
    hf_output_path = os.path.join(project_root, 'data', 'huggingface_finetuning.json')
    finetuning_prep.prepare_for_huggingface_finetuning(hf_output_path)