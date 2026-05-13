#!/bin/bash

PYTHON_SCRIPT="main.py"
PYTHON_ARGS="--local"

echo "Running $PYTHON_SCRIPT with arguments: $PYTHON_ARGS"

python3 -O "$PYTHON_SCRIPT" $PYTHON_ARGS 2>&1

if [ $? -ne 0 ]; then
    echo
    echo "Python script failed with errorlevel $?"
fi
