#!/bin/bash
# Launcher script for Mobile UI JSON Editor

echo "Mobile UI JSON Editor"
echo "====================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if PyQt5 is installed
python3 -c "import PyQt5" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "PyQt5 is not installed. Installing now..."
    pip install PyQt5==5.15.10
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install PyQt5"
        echo "Please run: pip install PyQt5==5.15.10"
        exit 1
    fi
fi

# Run the application
echo "Starting Mobile UI JSON Editor..."
python3 mobile_ui_editor.py
