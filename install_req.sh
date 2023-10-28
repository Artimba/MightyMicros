#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found. Please install Python 3."
    exit 1
fi

# Create a virtual environment
python3 -m venv mighty

# Activate the virtual environment
source mighty/bin/activate

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    # Install dependencies from requirements.txt
    pip install -r requirements.txt
else
    echo "requirements.txt not found."
fi

# Deactivate the virtual environment
deactivate
