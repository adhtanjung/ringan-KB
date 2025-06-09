import pandas as pd
import sys
from typing import List, Dict, Union, get_origin, get_args
from dataclasses import dataclass, field, fields, MISSING
from src.models import Problem, SelfAssessment, Suggestion, FeedbackPrompt, NextAction, FinetuningExample

class DataLoader:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        try:
            self.xlsx = pd.ExcelFile(excel_path)
        except FileNotFoundError:
            print(f"Error: Excel file not found at {excel_path}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error opening Excel file: {e}", file=sys.stderr)
            sys.exit(1)

    def _load_sheet(self, sheet_name: str, model_class: type):
        try:
            df = pd.read_excel(self.xlsx, sheet_name=sheet_name)
            records = []

            # Get the primary key field name (first field in the dataclass)
            pk_field = fields(model_class)[0].name

            # Drop rows where the primary key is NaN, indicating an empty or malformed row
            if pk_field in df.columns:
                df.dropna(subset=[pk_field], inplace=True)

            for index, row in df.iterrows():
                record_data = {}
                for field_info in fields(model_class):
                    col_name_in_excel = field_info.name
                    # Handle specific column name mappings if different from model
                    if field_info.name == 'conversation_id':
                        col_name_in_excel = 'ConversationID'

                    # Check if the column exists in the DataFrame
                    if col_name_in_excel not in row.index:
                        # If a required field is missing, raise an error
                        if field_info.default is MISSING and not (get_origin(field_info.type) is Union and type(None) in get_args(field_info.type)):
                            raise ValueError(f"Missing required column '{col_name_in_excel}' in sheet '{sheet_name}' for row {index}")
                        else:
                            # For optional fields, assign None or default value
                            record_data[field_info.name] = None if (get_origin(field_info.type) is Union and type(None) in get_args(field_info.type)) else field_info.default
                            continue

                    value = row[col_name_in_excel]

                    if pd.isna(value):
                        # Handle NaN values
                        if field_info.default is MISSING and not (get_origin(field_info.type) is Union and type(None) in get_args(field_info.type)):
                            # If it's a required field and NaN, raise an error
                            raise ValueError(f"NaN value found for required field '{field_info.name}' in sheet '{sheet_name}' at row {index}")
                        else:
                            # For optional fields, assign None
                            record_data[field_info.name] = None
                    else:
                        # Assign non-NaN value, with type conversion for specific fields
                        if field_info.name in ['id', 'conversation_id', 'problem']:
                            record_data[field_info.name] = str(value)
                        else:
                            record_data[field_info.name] = value

                records.append(model_class(**record_data))
            return records
        except KeyError as e:
            print(f"Error loading sheet '{sheet_name}': Column '{e}' not found or incorrectly accessed.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error loading sheet '{sheet_name}': {e}", file=sys.stderr)
            sys.exit(1)

    def load_problems(self) -> List[Problem]:
        return self._load_sheet('1.1 Problems', Problem)

    def load_self_assessments(self) -> List[SelfAssessment]:
        return self._load_sheet('1.2 Self Assessment', SelfAssessment)

    def load_suggestions(self) -> List[Suggestion]:
        return self._load_sheet('1.3 Suggestions', Suggestion)

    def load_feedback_prompts(self) -> List[FeedbackPrompt]:
        return self._load_sheet('1.4 Feedback Prompts', FeedbackPrompt)

    def load_next_actions(self) -> List[NextAction]:
        return self._load_sheet('1.5 Next Action After Feedback', NextAction)

    def load_finetuning_examples(self) -> List[FinetuningExample]:
        return self._load_sheet('1.6 FineTuning Examples', FinetuningExample)

    def load_all_data(self) -> Dict[str, List]:
        return {
            "problems": self.load_problems(),
            "self_assessments": self.load_self_assessments(),
            "suggestions": self.load_suggestions(),
            "feedback_prompts": self.load_feedback_prompts(),
            "next_actions": self.load_next_actions(),
            "finetuning_examples": self.load_finetuning_examples()
        }