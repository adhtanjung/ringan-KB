#!/bin/bash

# Ringan Mental Health Knowledge Base Launcher
# This script provides a simple way to run the Ringan KB application

# Set text colors
GREEN="\033[0;32m"
CYAN="\033[0;36m"
YELLOW="\033[0;33m"
NC="\033[0m" # No Color

# Display header
echo -e "\n${CYAN}=========================================================${NC}"
echo -e "${CYAN}       RINGAN MENTAL HEALTH KNOWLEDGE BASE${NC}"
echo -e "${CYAN}=========================================================${NC}\n"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check for broken virtual environment and remove it if necessary
if [ -d "venv" ]; then
    echo "Checking existing virtual environment..."
    if ! venv/bin/python3 --version >/dev/null 2>&1; then
        echo -e "${YELLOW}Broken virtual environment detected. Removing it...${NC}"
        rm -rf venv
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    # Use the system Python 3.9 to create the virtual environment
    python3 -m venv venv
    
    # Check if venv creation was successful
    if [ ! -d "venv/bin" ] || ! venv/bin/python3 --version >/dev/null 2>&1; then
        echo -e "${YELLOW}Warning: Could not create virtual environment. Proceeding with system Python.${NC}"
        # Set variables to use system Python instead of venv
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    else
        echo -e "${GREEN}Virtual environment created successfully.${NC}"
        PYTHON_CMD="venv/bin/python3"
        PIP_CMD="venv/bin/pip3"
    fi
else
    # Virtual environment exists and is valid
    PYTHON_CMD="venv/bin/python3"
    PIP_CMD="venv/bin/pip3"
fi

# Activate virtual environment if it exists and is valid
if [ -d "venv/bin" ] && [ -f "venv/bin/python3" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo -e "${GREEN}Virtual environment activated.${NC}"
else
    echo -e "${YELLOW}Warning: Cannot activate virtual environment. Using system Python.${NC}"
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
fi

# Check and install requirements if needed
echo "Checking installation..."
if [ -f "requirements.txt" ]; then
    echo "Installing/Updating required packages..."
    $PIP_CMD install -r requirements.txt
    
    # Verify installation
    if ! $PYTHON_CMD -c "import pandas" 2>/dev/null; then
        echo -e "${YELLOW}Warning: Failed to install packages with $PIP_CMD. Trying with pip3...${NC}"
        pip3 install -r requirements.txt
        
        # If system pip3 was used, we need to make sure we use system python3 for execution
        if ! $PYTHON_CMD -c "import pandas" 2>/dev/null; then
            echo -e "${YELLOW}Using system Python for execution since packages were installed there.${NC}"
            PYTHON_CMD="python3"
        fi
    fi
fi

# Try to run check_installation.py
$PYTHON_CMD check_installation.py 2>/dev/null || python3 check_installation.py 2>/dev/null || echo -e "${YELLOW}Warning: Could not run check_installation.py${NC}"

# Display menu
echo -e "\n${CYAN}Choose an option:${NC}"
echo -e "  ${GREEN}1${NC}. Setup database and vector store"
echo -e "  ${GREEN}2${NC}. Start interactive chat"
echo -e "  ${GREEN}3${NC}. Generate knowledge base report"
echo -e "  ${GREEN}4${NC}. Start API server (Uvicorn)"
echo -e "  ${GREEN}5${NC}. Start frontend server"
echo -e "  ${GREEN}6${NC}. Run all components (setup, verify, demo, report)"
echo -e "  ${GREEN}7${NC}. Exit"

read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        echo "Setting up database and vector store..."
        $PYTHON_CMD ringan_kb.py --setup || python3 ringan_kb.py --setup
        ;;
    2)
        echo "Starting interactive chat..."
        $PYTHON_CMD ringan_kb.py --chat || python3 ringan_kb.py --chat
        ;;
    3)
        echo "Generating knowledge base report..."
        $PYTHON_CMD ringan_kb.py --report || python3 ringan_kb.py --report
        ;;
    4)
        echo "Starting API server (Uvicorn)..."
        if [ -d "venv/bin" ] && [ -f "venv/bin/uvicorn" ]; then
            venv/bin/uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
        else
            # Try system uvicorn
            if command -v uvicorn &> /dev/null; then
                uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
            else
                echo -e "${YELLOW}Error: Uvicorn not found. Please install it with 'pip3 install uvicorn'.${NC}"
                exit 1
            fi
        fi
        ;;
    5)
        echo "Starting frontend server..."
        $PYTHON_CMD ringan_kb.py --frontend || python3 ringan_kb.py --frontend
        ;;
    6)
        echo "Running all components..."
        # Try with configured Python command first, fall back to system Python if that fails
        $PYTHON_CMD ringan_kb.py --all || python3 ringan_kb.py --all
        ;;
    7)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo -e "${YELLOW}Invalid choice. Please run the script again.${NC}"
        exit 1
        ;;
esac

# Deactivate virtual environment if it was activated
if [ -d "venv" ]; then
    deactivate 2>/dev/null || true
fi

echo -e "\n${GREEN}Done!${NC}"