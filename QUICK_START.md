# Ringan Mental Health Knowledge Base - Quick Start Guide

This guide will help you get started with the Ringan Mental Health Knowledge Base system quickly.

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Quick Setup

### Option 1: Using the Shell Script (Recommended)

The easiest way to get started is to use the provided shell script:

```bash
# Make the script executable (if not already)
chmod +x run.sh

# Run the launcher script
./run.sh
```

The script will guide you through the setup process with a simple menu interface.

### Option 2: Using the Python Script Directly

Alternatively, you can use the Python script directly:

```bash
# Check your installation
python check_installation.py

# Set up the database and vector store (run this first)
python ringan_kb.py --setup

# Start an interactive chat session
python ringan_kb.py --chat
```

## Common Tasks

### Setting Up the Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Running the System

- **Interactive Chat**: Talk directly with the AI assistant
  ```bash
  python ringan_kb.py --chat
  ```

- **Generate Report**: Create a visual report of knowledge base usage
  ```bash
  python ringan_kb.py --report
  ```

- **API Server**: Start the backend API server
  ```bash
  python ringan_kb.py --api
  ```

- **Frontend**: Start the web interface
  ```bash
  python ringan_kb.py --frontend
  ```

## Troubleshooting

If you encounter any issues:

1. Run the installation check script:
   ```bash
   python check_installation.py
   ```

2. Ensure your OpenAI API key is correctly set in the `.env` file

3. Try reinitializing the database:
   ```bash
   python ringan_kb.py --setup
   ```

For more detailed information, refer to the full README.md file.