#!/bin/bash

# Exit on error
set -e

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi

    # Activate virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate

    # Upgrade pip
    echo "Upgrading pip..."
    pip install --upgrade pip

    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt

    # Install package in development mode
    echo "Installing BookWright in development mode..."
    pip install -e .
fi

# Run the application
echo "Starting BookWright..."
bookwright
