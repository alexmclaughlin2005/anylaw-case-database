# Local Development Guide

This guide will help you run AnyLaw locally for development and testing.

## Prerequisites

- Python 3.11+ installed
- Git installed
- Terminal/Command Prompt

## Quick Start

### Option 1: Use Helper Scripts (Recommended)

#### Start Backend (Terminal 1)
```bash
cd "/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw"
chmod +x start-backend.sh
./start-backend.sh
```

This will:
- Create a virtual environment if needed
- Install dependencies
- Create data symlink if needed
- Start the backend on `http://localhost:5000`

#### Start Frontend (Terminal 2)
```bash
cd "/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw"
chmod +x start-frontend.sh
./start-frontend.sh
```

This will:
- Start a simple HTTP server on `http://localhost:8080`
- Serve the frontend static files

#### Access the Application
Open your browser and visit: `http://localhost:8080`

### Option 2: Manual Setup

#### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create data symlink (if not exists)
ln -s "../Anylaw sample documents-b" data

# Set environment variables
export FLASK_ENV=development
export CORS_ORIGINS="http://localhost:8080,http://127.0.0.1:8080"
export DATA_DIR="data"

# Run the application
python app.py
```

Backend will be available at `http://localhost:5000`

#### Frontend Setup

```bash
# In a new terminal
cd frontend

# Start HTTP server
python3 -m http.server 8080

# OR use any other static server:
# npx serve -p 8080
# php -S localhost:8080
```

Frontend will be available at `http://localhost:8080`

## Verify Installation

### Test Backend

Open a new terminal and run:

```bash
# Health check
curl http://localhost:5000/health

# Should return:
# {"status":"healthy","service":"anylaw-backend","version":"1.0.0"}

# Get statistics
curl http://localhost:5000/api/stats

# Search
curl http://localhost:5000/api/search?q=test
```

### Test Frontend

1. Open browser to `http://localhost:8080`
2. Dashboard should load with statistics
3. Navigate to Search page
4. Try searching for a case
5. Click on a case to view details

## Development Workflow

### Making Backend Changes

1. Edit files in `backend/`
2. Save changes
3. Backend auto-reloads (Flask debug mode)
4. Test API endpoints with curl or browser

### Making Frontend Changes

1. Edit files in `frontend/`
2. Save changes
3. Refresh browser to see changes
4. Check browser console for errors

### Making Data Changes

Data files are read-only. The backend caches the index, so if you modify data:

1. Restart the backend server
2. Cache will be refreshed on startup

## Project Structure for Development

```
backend/
  app.py              ← Edit for API changes
  requirements.txt    ← Add Python dependencies here

frontend/
  *.html             ← Edit for page structure
  static/css/        ← Edit for styling
  static/js/api.js   ← Edit for API client
  static/js/main.js  ← Edit for utilities
  env.js             ← Configure API URL
```

## Environment Configuration

### Backend Environment Variables

For local development, these are set in the start script:

```bash
FLASK_ENV=development          # Enables debug mode
CORS_ORIGINS=http://localhost:8080  # Allows frontend to call API
DATA_DIR=data                  # Path to data directory
PORT=5000                      # Port to run on
```

### Frontend Configuration

Edit `frontend/env.js`:

```javascript
window.ENV = {
    API_URL: 'http://localhost:5000'  // Local backend
};
```

## Common Issues

### "Port already in use"

If you see "Address already in use" errors:

**Backend (Port 5000)**
```bash
# Find process
lsof -i :5000

# Kill it
kill -9 <PID>
```

**Frontend (Port 8080)**
```bash
# Find process
lsof -i :8080

# Kill it
kill -9 <PID>
```

### "Data directory not found"

```bash
cd backend
ln -s "../Anylaw sample documents-b" data
ls -la data  # Verify symlink
```

### "Module not found" (Python)

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### CORS Errors in Browser

1. Check backend is running
2. Verify CORS_ORIGINS includes `http://localhost:8080`
3. Restart backend after changing CORS settings
4. Check browser console for exact error

### API Connection Failed

1. Verify backend is running: `curl http://localhost:5000/health`
2. Check `frontend/env.js` has correct URL
3. Check browser console network tab
4. Verify no firewall blocking

## Debugging

### Backend Debugging

The backend runs with Flask's debug mode enabled locally:

```python
# In app.py, this is enabled for local dev:
app.run(debug=True, host='0.0.0.0', port=port)
```

This provides:
- Auto-reload on code changes
- Detailed error pages
- Stack traces in browser

### Frontend Debugging

Use browser developer tools:

1. **Console**: `Cmd+Option+J` (Mac) or `F12` (Windows)
   - View JavaScript errors
   - See API call logs
   - Check loaded resources

2. **Network Tab**: View API requests
   - See request/response
   - Check status codes
   - Verify CORS headers

3. **Sources Tab**: Set breakpoints
   - Debug JavaScript code
   - Step through execution

### Logging

**Backend Logs**: Appear in the terminal running `python app.py`

**Frontend Logs**: Appear in browser console

## Testing Changes

### Before Committing

1. Test all features:
   - Dashboard loads
   - Search works
   - Citation lookup works
   - Case detail loads
   - Navigation works

2. Check for errors:
   - No backend errors in terminal
   - No frontend errors in console
   - All API calls succeed

3. Test edge cases:
   - Empty search
   - Invalid citation
   - Non-existent case ID
   - Special characters in search

## Database Queries

The application uses in-memory indexing. To see what's loaded:

```python
# In backend/app.py, add temporary debug code:

@app.route('/debug/index')
def debug_index():
    return jsonify({
        'total_documents': len(db.index),
        'sample': db.index[0] if db.index else None
    })
```

Then visit: `http://localhost:5000/debug/index`

## Performance Testing

### Backend Performance

```bash
# Simple load test with curl
for i in {1..100}; do
  curl http://localhost:5000/api/stats &
done
wait
```

### Frontend Performance

Use browser DevTools:
1. Open Network tab
2. Disable cache
3. Reload page
4. Check load times
5. Optimize slow resources

## Hot Reload Setup

### Backend (Already Enabled)
Flask debug mode auto-reloads on file changes.

### Frontend
Use a live reload server:

```bash
npm install -g live-server
cd frontend
live-server --port=8080
```

Now frontend auto-reloads on file changes.

## Next Steps

Once you're comfortable with local development:

1. Review [DEPLOYMENT_PLAN.md](DEPLOYMENT_PLAN.md) for deployment architecture
2. Follow [GITLAB_DEPLOYMENT_GUIDE.md](GITLAB_DEPLOYMENT_GUIDE.md) to deploy
3. Set up continuous deployment with GitLab

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Chart.js Documentation: https://www.chartjs.org/
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

---

Happy coding! 🚀

