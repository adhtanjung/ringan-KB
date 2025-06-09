import pandas as pd
from sqlalchemy import create_engine, Column, String, Text, ForeignKey, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from .data_preprocessing import DataPreprocessor

Base = declarative_base()

class Problem(Base):
    __tablename__ = 'problems'

    problem_id = Column(String(10), primary_key=True)
    problem_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    self_assessments = relationship("SelfAssessment", back_populates="problem")
    suggestions = relationship("Suggestion", back_populates="problem")

class SelfAssessment(Base):
    __tablename__ = 'self_assessments'

    question_id = Column(String(10), primary_key=True)
    problem_id = Column(String(10), ForeignKey('problems.problem_id'), nullable=False)
    question_text = Column(Text, nullable=False)
    response_type = Column(String(50), nullable=False)
    next_step = Column(String(50), nullable=True)

    # Relationships
    problem = relationship("Problem", back_populates="self_assessments")

class Suggestion(Base):
    __tablename__ = 'suggestions'

    suggestion_id = Column(String(10), primary_key=True)
    problem_id = Column(String(10), ForeignKey('problems.problem_id'), nullable=False)
    suggestion_text = Column(Text, nullable=False)
    resource_link = Column(String(255), nullable=True)

    # Relationships
    problem = relationship("Problem", back_populates="suggestions")

class FeedbackPrompt(Base):
    __tablename__ = 'feedback_prompts'

    prompt_id = Column(String(10), primary_key=True)
    stage = Column(String(50), nullable=False)
    prompt_text = Column(Text, nullable=False)
    next_action = Column(String(10), ForeignKey('next_actions.action_id'), nullable=True)

class NextAction(Base):
    __tablename__ = 'next_actions'

    action_id = Column(String(10), primary_key=True)
    label = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    feedback_prompts = relationship("FeedbackPrompt", backref="action")

class FinetuningExample(Base):
    __tablename__ = 'finetuning_examples'

    id = Column(String(10), primary_key=True)
    prompt = Column(Text, nullable=False)
    completion = Column(Text, nullable=False)
    problem = Column(String(10), ForeignKey('problems.problem_id'), nullable=True)
    conversation_id = Column(String(50), nullable=True)

def create_tables(engine):
    """Create all tables in the database"""
    Base.metadata.create_all(engine)

def load_dataframes_to_db(engine, dataframes):
    """Load processed DataFrames into the database"""
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Load Problems
        for _, row in dataframes['problems'].iterrows():
            problem = Problem(
                problem_id=row['problem_id'],
                problem_name=row['problem_name'],
                description=row.get('description')
            )
            session.add(problem)

        # Load Self Assessments
        for _, row in dataframes['self_assessments'].iterrows():
            assessment = SelfAssessment(
                question_id=row['question_id'],
                problem_id=row['problem_id'],
                question_text=row['question_text'],
                response_type=row['response_type'],
                next_step=row.get('next_step')
            )
            session.add(assessment)

        # Load Suggestions
        for _, row in dataframes['suggestions'].iterrows():
            suggestion = Suggestion(
                suggestion_id=row['suggestion_id'],
                problem_id=row['problem_id'],
                suggestion_text=row['suggestion_text'],
                resource_link=row.get('resource_link')
            )
            session.add(suggestion)

        # Load Feedback Prompts
        for _, row in dataframes['feedback_prompts'].iterrows():
            prompt = FeedbackPrompt(
                prompt_id=row['prompt_id'],
                stage=row['stage'],
                prompt_text=row['prompt_text'],
                next_action=row.get('next_action')
            )
            session.add(prompt)

        # Load Next Actions
        for _, row in dataframes['next_actions'].iterrows():
            action = NextAction(
                action_id=row['action_id'],
                label=row['label'],
                description=row.get('description')
            )
            session.add(action)

        # Load Finetuning Examples
        for _, row in dataframes['finetuning_examples'].iterrows():
            example = FinetuningExample(
                id=row['id'],
                prompt=row['prompt'],
                completion=row['completion'],
                problem=row.get('problem'),
                conversation_id=row.get('conversation_id')
            )
            session.add(example)

        session.commit()
        print("All data loaded successfully")
    except Exception as e:
        session.rollback()
        print(f"Error loading data: {e}")
    finally:
        session.close()

# Example usage
if __name__ == "__main__":
    import os

    # Setup database
    engine = create_engine('sqlite:///mental_health_kb.db')
    create_tables(engine)

    # Load and process data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    excel_file_path = os.path.join(project_root, 'data', 'missing_values_updated.xlsx')

    preprocessor = DataPreprocessor(excel_file_path)
    knowledge_base = preprocessor.load_and_process_all_sheets()

    # Load data into database
    load_dataframes_to_db(engine, knowledge_base)