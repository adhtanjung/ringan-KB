import os
import sys
from pathlib import Path
from sqlalchemy import create_engine

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.db_schema import Base, create_tables

def main():
    # Get the absolute path to the database file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    db_path = os.path.join(project_root, 'mental_health_kb.db')
    
    # Create engine and update tables
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Drop all tables and recreate them
    print("Dropping existing tables...")
    Base.metadata.drop_all(engine)
    
    print("Creating new tables...")
    create_tables(engine)
    
    print("Database schema updated successfully!")

if __name__ == "__main__":
    main()
