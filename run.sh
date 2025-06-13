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

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Would you like to create one? (y/n)${NC}"
    read -r create_venv
    if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        echo -e "${GREEN}Virtual environment created.${NC}"
    else
        echo "Proceeding without virtual environment."
    fi
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo -e "${GREEN}Virtual environment activated.${NC}"
fi

# Check if requirements are installed
echo "Checking installation..."
python3 check_installation.py

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
        python3 ringan_kb.py --setup
        ;;
    2)
        echo "Starting interactive chat..."
        python3 ringan_kb.py --chat
        ;;
    3)
        echo "Generating knowledge base report..."
        python3 ringan_kb.py --report
        ;;
    4)
        echo "Starting API server (Uvicorn)..."
        uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
        ;;
    5)
        echo "Starting frontend server..."
        python3 ringan_kb.py --frontend
        ;;
    6)
        echo "Running all components..."
        python3 ringan_kb.py --all
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