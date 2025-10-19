#!/bin/bash
set -e  # Exit immediately if any command fails

echo "Setting up Python environment for deployment..."

# Check if .venv exists in current or parent directory
if [ ! -d ".venv" ] && [ ! -d "../.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "../.venv" ]; then
    source ../.venv/bin/activate
else
    echo "Could not find virtual environment directory."
    exit 1
fi

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r ../requirements.txt

echo "Environment setup complete."
