#!/bin/bash

echo "export PYTHONPATH=/weatherbot" >> ~/.bashrc && . ~/.bashrc

# --- 
echo "Waiting for MySQL..."

while ! nc -z db 3306; do
  sleep 0.5
done

echo "MySQL started"

# ---
cd src/
uvicorn weatherbot:app --host 0.0.0.0 --port 5000
