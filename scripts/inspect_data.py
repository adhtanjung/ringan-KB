import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.data_loader import DataLoader

def main():
    # Load and process the Excel file
    excel_file = project_root / 'data' / 'missing_values_updated.xlsx'
    data_loader = DataLoader(excel_file)
    knowledge_base = data_loader.load_all_data()
    
    # Print the structure of the knowledge base
    print("Knowledge base keys:", knowledge_base.keys())
    
    # Print the type and first few items of each key
    for key, value in knowledge_base.items():
        print(f"\n--- {key} ---")
        print(f"Type: {type(value)}")
        if isinstance(value, list):
            print(f"Length: {len(value)}")
            if len(value) > 0:
                print("First item:", value[0])
        elif hasattr(value, 'head'):  # For DataFrames
            print(f"Shape: {value.shape}")
            print("Columns:", value.columns.tolist())
            print("First row:", value.iloc[0].to_dict() if len(value) > 0 else "Empty")
        else:
            print("Value:", value)

if __name__ == "__main__":
    main()
