# Expanded Mental Health Knowledge Base

This directory contains the expanded mental health knowledge base data used by the Ringan application.

## Files

- `expanded_mental_health_kb_data.xlsx`: Comprehensive Excel file containing expanded mental health data
- `vector_db/`: Directory containing the vector database with embeddings for efficient retrieval

## Data Structure

The Excel file contains the following sheets:

1. **Problems**: Mental health issues with descriptions
2. **SelfAssessment**: Assessment questions for each problem
3. **Suggestions**: Coping strategies and resources for each problem
4. **FeedbackPrompts**: Conversation prompts for different stages of interaction
5. **NextActions**: Possible next steps in the conversation flow
6. **FinetuningExamples**: Example conversations for fine-tuning the model

## Integration Process

The expanded knowledge base was integrated into the project using the following steps:

1. Generated the expanded Excel file using `src/expanded_data_model.py`
2. Updated the vector database with the expanded data using `scripts/update_kb_with_expanded_data.py`

## Usage

The expanded knowledge base provides more comprehensive mental health information, including:

- 15 mental health problems (anxiety, depression, stress, etc.)
- Detailed assessment questions for each problem
- Specific coping strategies and resources
- Conversation prompts and flow guidance

This expanded data enhances the application's ability to provide relevant and helpful responses to users seeking mental health support.