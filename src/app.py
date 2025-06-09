import sys
import os
from src.data_loader import DataLoader

def main():
    # Construct the absolute path to the Excel file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    excel_file_path = os.path.join(project_root, 'data', 'missing_values_updated.xlsx')

    print(f"Current working directory: {os.getcwd()}")
    print(f"Attempting to open Excel file at: {excel_file_path}")

    try:
        data_loader = DataLoader(excel_file_path)

        print("Loading data from Excel file...")
        knowledge_base = data_loader.load_all_data()

        print(f"Loaded {len(knowledge_base['problems'])} problems.")
        print(f"Loaded {len(knowledge_base['self_assessments'])} self-assessments.")
        print(f"Loaded {len(knowledge_base['suggestions'])} suggestions.")
        print(f"Loaded {len(knowledge_base['feedback_prompts'])} feedback prompts.")
        print(f"Loaded {len(knowledge_base['next_actions'])} next actions.")
        print(f"Loaded {len(knowledge_base['finetuning_examples'])} finetuning examples.")

        # You can now access your data like this:
        # for problem in knowledge_base['problems']:
        #     print(f"Problem: {problem.problem_name}")

        # Further application logic will go here.
        print("\nData loading complete. You can now build your AI application logic around this knowledge base.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()