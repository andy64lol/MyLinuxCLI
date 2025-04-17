#!/bin/bash

echo "Running the math game..."
# A simple wrapper to run the Python math game
python3 math_game.py "$@" || { echo "Failed to run math_game.py"; exit 1; }
