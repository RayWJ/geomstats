#!/bin/bash
# Start script for Cognitive Physics Engine

echo "🌍 Starting Cognitive Physics Engine..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
cd backend
pip install -q -r requirements.txt

# Start the server
echo ""
echo "✓ Starting FastAPI server on http://localhost:8000"
echo "✓ Frontend available at: cognitive_physics_engine/frontend/index.html"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python server.py
