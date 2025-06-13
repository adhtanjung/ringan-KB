#!/usr/bin/env python3

import os
import sys
import importlib
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
try:
    init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False

# Define color functions that work even if colorama is not installed
def green(text):
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}" if COLORS_AVAILABLE else text

def red(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}" if COLORS_AVAILABLE else text

def yellow(text):
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}" if COLORS_AVAILABLE else text

def cyan(text):
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}" if COLORS_AVAILABLE else text

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  {green('✓')} Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  {red('✗')} Python version: {version.major}.{version.minor}.{version.micro} (3.8+ required)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("Checking required packages...")
    required_packages = [
        'pandas',
        'sqlalchemy',
        'sentence_transformers',
        'langchain',
        'langchain_openai',
        'langchain_community',
        'openai',
        'fastapi',
        'uvicorn',
        'chromadb',
        'tabulate',
        'colorama'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"  {green('✓')} {package}")
        except ImportError:
            print(f"  {red('✗')} {package} (not installed)")
            all_installed = False
    
    return all_installed

def check_openai_api_key():
    """Check if OpenAI API key is set"""
    print("Checking OpenAI API key...")
    api_key = os.environ.get('OPENAI_API_KEY')
    
    # Check for .env file
    env_file = Path('.env')
    env_file_exists = env_file.exists()
    
    if api_key:
        print(f"  {green('✓')} OPENAI_API_KEY environment variable is set")
        return True
    elif env_file_exists:
        print(f"  {yellow('!')} OPENAI_API_KEY not found in environment, but .env file exists")
        print(f"      Make sure the .env file contains: OPENAI_API_KEY=your_key_here")
        return True
    else:
        print(f"  {red('✗')} OPENAI_API_KEY not found in environment")
        print(f"      Create a .env file with: OPENAI_API_KEY=your_key_here")
        return False

def check_database():
    """Check if the database file exists"""
    print("Checking database file...")
    db_path = Path('mental_health_kb.db')
    if db_path.exists():
        print(f"  {green('✓')} Database file found: {db_path}")
        return True
    else:
        print(f"  {yellow('!')} Database file not found: {db_path}")
        print(f"      Run 'python ringan_kb.py --setup' to create the database")
        return False

def check_vector_db():
    """Check if the vector database exists"""
    print("Checking vector database...")
    vector_db_path = Path('data/vector_db')
    if vector_db_path.exists() and any(vector_db_path.iterdir()):
        print(f"  {green('✓')} Vector database found: {vector_db_path}")
        return True
    else:
        print(f"  {yellow('!')} Vector database not found or empty: {vector_db_path}")
        print(f"      Run 'python ringan_kb.py --setup' to create the vector database")
        return False

def main():
    print(cyan("\n=== Ringan Mental Health Knowledge Base - Installation Check ==="))
    
    # Run all checks
    python_ok = check_python_version()
    deps_ok = check_dependencies()
    api_key_ok = check_openai_api_key()
    db_ok = check_database()
    vector_db_ok = check_vector_db()
    
    # Summary
    print("\nSummary:")
    if all([python_ok, deps_ok, api_key_ok, db_ok, vector_db_ok]):
        print(green("✓ All checks passed! Your installation is ready to use."))
        print("\nYou can now run the application with:")
        print(cyan("  python ringan_kb.py --help"))
    else:
        print(yellow("! Some checks failed. Please address the issues above."))
        
        if not python_ok:
            print("  - Update Python to version 3.8 or higher")
        if not deps_ok:
            print("  - Install missing dependencies with: pip install -r requirements.txt")
        if not api_key_ok:
            print("  - Set up your OpenAI API key in a .env file")
        if not db_ok or not vector_db_ok:
            print("  - Initialize the database with: python ringan_kb.py --setup")

if __name__ == "__main__":
    main()