#!/bin/bash

# Usage: ./run_flake8.sh <path/to/file>
# Specify the path to a file or directory to analyze with flake8

# Extract the file or directory path from the command line argument
target_path="$1"

# Check if the argument is provided
if [ -z "$target_path" ]; then
    echo "Please provide the path to a file or directory to analyze."
    exit 1
fi

# Check if the path exists
if [ ! -e "$target_path" ]; then
    echo "The specified path does not exist."
    exit 1
fi

# Check if the path is a file or directory
if [ -f "$target_path" ]; then
    # If it's a file, analyze the file
    flake8 --format=html --output-file=flake8_report.html "$target_path"
else
    # If it's a directory, analyze all Python files in the directory
    flake8 --format=html --output-file=flake8_report.html "$target_path"
fi

