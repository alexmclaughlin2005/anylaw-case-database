#!/bin/bash
# AnyLaw Case Database Navigator - Start Script

echo "🚀 Starting AnyLaw Case Database Navigator..."
echo ""

# Check if data directory exists
if [ ! -d "Anylaw sample documents-b" ]; then
    echo "❌ Error: Data directory 'Anylaw sample documents-b' not found"
    exit 1
fi

# Check if index file exists
if [ ! -f "Anylaw sample documents-b/index.json" ]; then
    echo "❌ Error: Index file not found"
    exit 1
fi

# Check if requirements are installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Starting Flask server..."
echo "📍 Access the application at: http://localhost:5000"
echo "📍 Press Ctrl+C to stop the server"
echo ""

python3 app.py

