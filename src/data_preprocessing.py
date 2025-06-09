import pandas as pd
import numpy as np
import os
from typing import Dict, List

class DataPreprocessor:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        try:
            self.xlsx = pd.ExcelFile(excel_path)
            self.sheet_names = [
                '1.1 Problems',
                '1.2 Self Assessment',
                '1.3 Suggestions',
                '1.4 Feedback Prompts',
                '1.5 Next Action After Feedback',
                '1.6 FineTuning Examples'
            ]
        except FileNotFoundError:
            print(f"Error: Excel file not found at {excel_path}")
            raise
        except Exception as e:
            print(f"Error opening Excel file: {e}")
            raise

    def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names: lowercase, replace spaces with underscores, strip whitespace"""
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.strip()
        return df

    def remove_empty_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove columns that are entirely NaN"""
        return df.dropna(axis=1, how='all')

    def remove_empty_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove rows that are entirely NaN"""
        return df.dropna(axis=0, how='all')

    def fill_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fill missing values using mode imputation"""
        for column in df.columns:
            if df[column].isna().any():
                # For categorical/object columns
                if df[column].dtype == 'object' or df[column].dtype.name == 'category':
                    mode_value = df[column].mode()[0] if not df[column].mode().empty else ""
                    df[column] = df[column].fillna(mode_value)
                # For numeric columns
                else:
                    mode_value = df[column].mode()[0] if not df[column].mode().empty else 0
                    df[column] = df[column].fillna(mode_value)
        return df

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply all preprocessing steps to a DataFrame"""
        df = self.standardize_column_names(df)
        df = self.remove_empty_columns(df)
        df = self.remove_empty_rows(df)
        df = self.fill_missing_values(df)
        return df

    def load_and_process_all_sheets(self) -> Dict[str, pd.DataFrame]:
        """Load and process all sheets from the Excel file"""
        processed_data = {}

        for sheet_name in self.sheet_names:
            try:
                # Load the sheet
                df = pd.read_excel(self.xlsx, sheet_name=sheet_name)

                # Process the DataFrame
                processed_df = self.process_dataframe(df)

                # Handle specific sheet preprocessing (e.g., dropping duplicates for Feedback Prompts and Finetuning Examples)
                if sheet_name == '1.4 Feedback Prompts':
                    if 'prompt_id' in processed_df.columns:
                        processed_df = processed_df.drop_duplicates(subset=['prompt_id'])
                        print(f"Dropped duplicate prompt_ids in '1.4 Feedback Prompts'. New rows: {len(processed_df)}")
                elif sheet_name == '1.6 FineTuning Examples':
                    if 'id' in processed_df.columns:
                        # Drop rows where 'id' is NaN before dropping duplicates
                        processed_df = processed_df.dropna(subset=['id'])
                        processed_df = processed_df.drop_duplicates(subset=['id'])
                        print(f"Dropped rows with NaN ids and duplicate ids in '1.6 FineTuning Examples'. New rows: {len(processed_df)}")
                elif sheet_name == '1.3 Suggestions':
                    if 'suggestion_id' in processed_df.columns:
                        processed_df = processed_df.drop_duplicates(subset=['suggestion_id'])
                        print(f"Dropped duplicate suggestion_ids in '1.3 Suggestions'. New rows: {len(processed_df)}")

                # Store with a simplified key name
                key_mapping = {
                    '1.1 Problems': 'problems',
                    '1.2 Self Assessment': 'self_assessments',
                    '1.3 Suggestions': 'suggestions',
                    '1.4 Feedback Prompts': 'feedback_prompts',
                    '1.5 Next Action After Feedback': 'next_actions',
                    '1.6 FineTuning Examples': 'finetuning_examples'
                }
                key = key_mapping.get(sheet_name, sheet_name) # Fallback to original sheet name if not found
                processed_data[key] = processed_df

                print(f"Processed {sheet_name}: {len(processed_df)} rows, {len(processed_df.columns)} columns")
            except Exception as e:
                print(f"Error processing sheet {sheet_name}: {e}")

        return processed_data

# Example usage
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    excel_file_path = os.path.join(project_root, 'data', 'missing_values_updated.xlsx')

    preprocessor = DataPreprocessor(excel_file_path)
    knowledge_base = preprocessor.load_and_process_all_sheets()

    # Print summary of processed data
    for key, df in knowledge_base.items():
        print(f"\n{key.capitalize()} DataFrame:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {', '.join(df.columns)}")
        print(f"Sample data:\n{df.head(2)}")