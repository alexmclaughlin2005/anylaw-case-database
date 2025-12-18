# AnyLaw Deployment Plan

## Overview
This plan outlines the steps to deploy AnyLaw with a separated architecture:
- **Frontend**: Static site on Vercel (HTML/CSS/JavaScript)
- **Backend**: Flask API on Railway (Python)
- **Source Control**: GitLab

## Current Architecture
- Monolithic Flask app with server-side rendering (Jinja2)
- Templates served by Flask
- API endpoints already exist but mixed with template routes
- Static assets (CSS/JS) served by Flask

## Target Architecture

### Backend (Railway)
**Location**: `/backend/`
- Pure Flask REST API (no templates)
- CORS enabled for cross-origin requests from Vercel
- Serves JSON data only
- Handles all business logic and data processing
- Serves data files from `/backend/data/`

**Endpoints**:
- `GET /api/stats` - Database statistics
- `GET /api/jurisdictions` - List of jurisdictions
- `GET /api/search` - Search cases
- `GET /api/document/<id>` - Get full document
- `GET /api/citation/<citation>` - Find by citation
- `GET /api/citations` - List all citations
- `GET /health` - Health check endpoint

### Frontend (Vercel)
**Location**: `/frontend/`
- Static HTML/CSS/JavaScript
- No server-side rendering
- Calls backend API via fetch
- Environment variable for API URL
- Modern SPA (Single Page Application) behavior

**Pages**:
- `index.html` - Dashboard
- `search.html` - Search interface
- `case.html` - Case detail viewer

## Implementation Steps

### Phase 1: Project Restructuring ✅
1. Create `/backend/` directory
   - Move `app.py` → `backend/app.py` (modified for API-only)
   - Move `requirements.txt` → `backend/requirements.txt` (add flask-cors)
   - Move data → `backend/data/` (symlink or copy)
   - Create `backend/runtime.txt` for Python version
   - Create `backend/Procfile` for Railway

2. Create `/frontend/` directory
   - Move `templates/` → `frontend/` (convert to static HTML)
   - Move `static/` → `frontend/static/`
   - Create `frontend/vercel.json` for routing
   - Create `frontend/.env.example` for API URL

### Phase 2: Backend Modifications
1. Remove all template rendering routes
2. Add Flask-CORS for cross-origin requests
3. Update app to only serve API endpoints
4. Add health check endpoint for Railway
5. Configure for production (gunicorn)
6. Environment variables for configuration

### Phase 3: Frontend Modifications
1. Convert Jinja2 templates to pure HTML
2. Create API client module (`frontend/static/js/api.js`)
3. Update existing JavaScript to use API client
4. Handle environment variables for API endpoint
5. Implement client-side routing
6. Add loading states and error handling

### Phase 4: Deployment Configuration

#### Railway (Backend)
**File**: `backend/railway.json` or use Railway dashboard
- Set start command: `gunicorn app:app`
- Environment variables:
  - `PYTHON_VERSION=3.11`
  - `FLASK_ENV=production`
  - `CORS_ORIGINS=https://your-app.vercel.app`

**File**: `backend/Procfile`
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

**File**: `backend/requirements.txt`
```
Flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
Werkzeug==3.0.1
...
```

#### Vercel (Frontend)
**File**: `frontend/vercel.json`
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/$1" },
    { "source": "/", "destination": "/index.html" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
```

**File**: `frontend/.env.production`
```
VITE_API_URL=https://your-backend.railway.app
```

### Phase 5: GitLab Setup
1. Create `.gitignore`
2. Initialize git repository
3. Create GitLab repository
4. Push code to GitLab
5. Configure GitLab CI/CD (optional)

### Phase 6: Deployment
1. Deploy backend to Railway
   - Connect GitLab repository
   - Set root directory to `/backend`
   - Configure environment variables
   - Deploy and get URL

2. Deploy frontend to Vercel
   - Connect GitLab repository
   - Set root directory to `/frontend`
   - Add environment variable for backend URL
   - Deploy

3. Update CORS settings on backend with Vercel URL

## Environment Variables

### Backend (Railway)
```
FLASK_ENV=production
CORS_ORIGINS=https://anylaw.vercel.app
DATA_DIR=/app/data
PORT=8000
```

### Frontend (Vercel)
```
API_URL=https://anylaw.railway.app
```

## File Structure After Changes

```
/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw/
├── backend/
│   ├── app.py                      # API-only Flask app
│   ├── requirements.txt            # Python dependencies + gunicorn, flask-cors
│   ├── Procfile                    # Railway start command
│   ├── runtime.txt                 # Python version
│   ├── railway.json                # Railway config (optional)
│   └── data/                       # Symlink to ../Anylaw sample documents-b/
│       ├── index.json
│       └── doc_*.json
│
├── frontend/
│   ├── index.html                  # Dashboard (no Jinja2)
│   ├── search.html                 # Search page (no Jinja2)
│   ├── case.html                   # Case detail (no Jinja2)
│   ├── vercel.json                 # Vercel config
│   ├── .env.example                # Environment variable template
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── api.js              # NEW: API client
│           └── main.js             # Updated to use API
│
├── Anylaw sample documents-b/      # Original data (kept at root)
├── .gitignore                      # Git ignore file
├── README.md                       # Updated documentation
├── AI_Instructions.md              # Updated for new architecture
├── AI_System_Prompt.md             # Updated for new architecture
└── DEPLOYMENT_PLAN.md              # This file
```

## Testing Strategy

### Local Testing
1. Start backend: `cd backend && python app.py`
2. Start frontend: `cd frontend && python -m http.server 8080`
3. Test all features work with separated architecture

### Pre-deployment Checklist
- [ ] Backend responds to all API endpoints
- [ ] CORS headers are properly configured
- [ ] Frontend can connect to local backend
- [ ] All environment variables are documented
- [ ] Data files are accessible to backend
- [ ] Health check endpoint works
- [ ] Error handling is implemented

### Post-deployment Checklist
- [ ] Backend is running on Railway
- [ ] Frontend is deployed on Vercel
- [ ] API calls from frontend to backend work
- [ ] CORS is properly configured
- [ ] All features work in production
- [ ] Environment variables are set correctly

## Rollback Plan
- Keep current monolithic version in a separate branch
- Can quickly redeploy monolithic version if needed
- Data files remain unchanged

## Timeline
- Phase 1-3: 2-3 hours (restructuring and code changes)
- Phase 4: 30 minutes (deployment configs)
- Phase 5: 15 minutes (GitLab setup)
- Phase 6: 30 minutes (actual deployment)
- Testing: 1 hour

**Total estimated time**: 4-5 hours

## Next Steps
1. Begin Phase 1: Create directory structure
2. Implement backend changes (API-only)
3. Implement frontend changes (static + API calls)
4. Test locally
5. Create deployment configs
6. Push to GitLab
7. Deploy to Railway and Vercel

