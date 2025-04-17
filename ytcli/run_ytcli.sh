#!/bin/bash

# A simple shell wrapper

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it to run this script."
    exit 1
fi

# Run the hacker_simulator.py script with any provided arguments
python3 ytcli.py "$@"
