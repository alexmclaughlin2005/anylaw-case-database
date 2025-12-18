#!/bin/bash
# Start the backend server for local development

echo "🚀 Starting AnyLaw Backend API..."
echo ""

cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "⚠️  Warning: data directory not found"
    echo "Creating symlink..."
    ln -s "../Anylaw sample documents-b" data
fi

echo ""
echo "✅ Backend starting on http://localhost:5000"
echo "📍 Health check: http://localhost:5000/health"
echo "📍 API docs: See DEPLOYMENT_PLAN.md"
echo "📍 Press Ctrl+C to stop"
echo ""

# Set environment variables for local development
export FLASK_ENV=development
export CORS_ORIGINS="http://localhost:8080,http://127.0.0.1:8080"
export DATA_DIR="data"

# Run the app
python app.py

