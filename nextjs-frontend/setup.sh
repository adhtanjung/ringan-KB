#!/bin/bash

# Setup script for Ringan KB Next.js Frontend

echo "=== Setting up Ringan KB Next.js Frontend ==="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js before continuing."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install npm before continuing."
    exit 1
fi

# Install dependencies
echo "\nInstalling dependencies..."
npm install

# Create .env.local file if it doesn't exist
if [ ! -f .env.local ]; then
    echo "\nCreating .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    echo ".env.local file created with default API URL."
fi

echo "\n=== Setup Complete! ==="
echo "\nTo start the development server:"
echo "npm run dev"
echo "\nTo build for production:"
echo "npm run build"
echo "npm start"
echo "\nMake sure the Ringan KB backend is running with:"
echo "python ../ringan_kb.py --api"

echo "\nVisit http://localhost:8080 to access the frontend."