#!/bin/bash
venv_dir="mighty"

if [ ! -d "$venv_dir" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$venv_dir"
else
  echo "Virtual environment exists."
fi

echo "Activating virtual environment..."
source "$venv_dir/bin/activate"

if [ -f "requirements.txt" ]; then
  echo "Installing dependencies..."
  pip install -r requirements.txt
else
  echo "requirements.txt not found."
fi
