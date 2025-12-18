#!/bin/bash
# Start the frontend server for local development

echo "🚀 Starting AnyLaw Frontend..."
echo ""

cd "$(dirname "$0")/frontend"

echo "⚙️  Using local backend at http://localhost:5000"
echo ""
echo "✅ Frontend starting on http://localhost:8080"
echo "📍 Dashboard: http://localhost:8080/index.html"
echo "📍 Search: http://localhost:8080/search.html"
echo "📍 Press Ctrl+C to stop"
echo ""
echo "⚠️  Make sure backend is running! (Run ./start-backend.sh in another terminal)"
echo ""

# Start simple HTTP server
python3 -m http.server 8080

