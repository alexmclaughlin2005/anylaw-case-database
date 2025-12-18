# AnyLaw Case Database Navigator - AI System Prompt

## Project Overview
AnyLaw Case Database Navigator is a modern web application for browsing, searching, and analyzing the Lexsphere caselaw database. The application is built with a separated architecture optimized for cloud deployment with frontend on Vercel and backend on Railway.

## High-Level Architecture

### Separated Architecture (Current)

```
Frontend (Vercel)          Backend (Railway)           Data
┌──────────────┐          ┌─────────────────┐         ┌──────────────┐
│ Static HTML  │          │  Flask REST API │         │ JSON Files   │
│ CSS          │─────────▶│  + CORS         │────────▶│ 1000+ cases  │
│ JavaScript   │  Fetch   │  + Gunicorn     │  Read   │ index.json   │
└──────────────┘          └─────────────────┘         └──────────────┘
```

### Backend (Railway)
**Location**: `/backend/`
- Pure Flask REST API (no templates)
- CORS enabled for Vercel frontend
- Serves only JSON data
- Business logic and data processing
- Deployed via Railway with Gunicorn

**Key Files**:
- `app.py` - Main Flask API application
- `requirements.txt` - Python dependencies (Flask, flask-cors, gunicorn)
- `Procfile` - Railway deployment command
- `runtime.txt` - Python version specification
- `railway.json` - Railway configuration
- `data/` - Symlink to case data directory

### Frontend (Vercel)
**Location**: `/frontend/`
- Static HTML/CSS/JavaScript site
- No server-side rendering
- Calls backend API via fetch
- Environment variable for API URL
- Client-side routing

**Key Files**:
- `index.html` - Dashboard page
- `search.html` - Search interface
- `case.html` - Case detail viewer
- `env.js` - Environment configuration
- `vercel.json` - Vercel deployment config
- `static/css/style.css` - Styles
- `static/js/api.js` - API client module
- `static/js/main.js` - Utility functions

### Data Layer
**Location**: `/Anylaw sample documents-b/`
- 1000+ JSON files with case data
- `index.json` - Master index with metadata
- Accessed by backend via symlink or direct path
- Read-only data

## Directory Structure

```
/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw/
├── backend/                          # Backend API (Railway)
│   ├── app.py                       # Flask REST API
│   ├── requirements.txt             # Python deps
│   ├── Procfile                     # Railway start
│   ├── runtime.txt                  # Python version
│   ├── railway.json                 # Railway config
│   └── data/                        # → Anylaw sample documents-b/
│
├── frontend/                         # Frontend (Vercel)
│   ├── index.html                   # Dashboard
│   ├── search.html                  # Search page
│   ├── case.html                    # Case detail
│   ├── env.js                       # Environment vars
│   ├── vercel.json                  # Vercel config
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── api.js               # API client
│           └── main.js              # Utilities
│
├── Anylaw sample documents-b/        # Case data
│   ├── index.json
│   └── doc_*.json (1000+ files)
│
├── .gitignore                        # Git ignore rules
├── DEPLOYMENT_PLAN.md               # Architecture & deployment plan
├── GITLAB_DEPLOYMENT_GUIDE.md       # Step-by-step deployment guide
├── README_NEW.md                    # Updated README
├── AI_System_Prompt_Updated.md      # This file
└── AI_Instructions_Updated.md       # Detailed technical docs
```

## Key Features

1. **Dashboard** - Real-time statistics and visualizations
2. **Text Search** - Filter cases by title, jurisdiction, year
3. **Citation Lookup** - Find cases by legal citation
4. **Case Detail Viewer** - Full case info with citation cross-references
5. **Citation Navigation** - Click citations to view referenced cases

## Technology Stack

### Backend (Railway)
- **Language**: Python 3.11
- **Framework**: Flask 3.0
- **CORS**: flask-cors 4.0
- **Server**: Gunicorn (production)
- **Data**: JSON files

### Frontend (Vercel)
- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js 4.4
- **API Client**: Vanilla JS Fetch API
- **No Build Step**: Pure static files

### Deployment
- **Frontend**: Vercel (static hosting)
- **Backend**: Railway (Python hosting)
- **CI/CD**: Auto-deploy on git push
- **Source Control**: GitLab

## API Endpoints

All backend endpoints serve JSON:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check for Railway |
| `/api/stats` | GET | Database statistics |
| `/api/jurisdictions` | GET | List of jurisdictions |
| `/api/search` | GET | Search cases with filters |
| `/api/document/<id>` | GET | Get full document + citations |
| `/api/citation/<citation>` | GET | Find case by citation |
| `/api/citations` | GET | List all citations (limited) |

## Environment Variables

### Backend (Railway)
```bash
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend.vercel.app
DATA_DIR=/app/data
PORT=8000
```

### Frontend (Vercel)
```javascript
// env.js
window.ENV = {
    API_URL: 'https://your-backend.railway.app'
};
```

## Development Workflow

### Local Development
1. **Backend**: `cd backend && python app.py` (runs on :5000)
2. **Frontend**: `cd frontend && python -m http.server 8080` (runs on :8080)
3. Frontend calls backend at `http://localhost:5000`

### Deployment Workflow
1. Make changes to code
2. Commit and push to GitLab: `git push origin main`
3. Railway auto-deploys backend (if backend/* changed)
4. Vercel auto-deploys frontend (if frontend/* changed)

## Maintenance Instructions

### Creating/Updating Documentation Files

When modifying this project, always maintain:

1. **AI_System_Prompt_Updated.md** (this file)
   - High-level overview
   - Architecture diagram
   - Directory structure
   - Update when: major architecture changes, new deployment targets

2. **AI_Instructions_Updated.md**
   - Detailed technical documentation
   - API specifications
   - Component descriptions
   - Code patterns and examples
   - Update when: any code changes, new features, API modifications

3. **README_NEW.md**
   - User-facing documentation
   - Quick start guide
   - Deployment instructions
   - Update when: setup process changes, new features added

4. **DEPLOYMENT_PLAN.md**
   - Deployment strategy and planning
   - Architecture decisions
   - Migration steps
   - Update when: deployment strategy changes

5. **GITLAB_DEPLOYMENT_GUIDE.md**
   - Step-by-step deployment instructions
   - Platform-specific guides
   - Troubleshooting
   - Update when: deployment platforms change, new steps added

## File Purposes

### Backend Files
- **app.py** - Flask API application with all endpoints
- **requirements.txt** - Python dependencies for Railway
- **Procfile** - Railway startup command (gunicorn)
- **runtime.txt** - Python version for Railway
- **railway.json** - Railway deployment configuration

### Frontend Files
- **index.html** - Dashboard with stats and charts
- **search.html** - Search and citation lookup interface
- **case.html** - Case detail page with citations
- **env.js** - Environment configuration (API URL)
- **vercel.json** - Vercel routing and configuration
- **static/css/style.css** - All styles (responsive)
- **static/js/api.js** - Backend API client
- **static/js/main.js** - Utility functions

### Deployment Files
- **.gitignore** - Git exclusions
- **DEPLOYMENT_PLAN.md** - Architecture plan
- **GITLAB_DEPLOYMENT_GUIDE.md** - Deployment guide

## Important Notes

### Backend
- No template rendering (API only)
- CORS must match frontend URL exactly
- Data directory accessed via symlink
- Gunicorn for production (handles multiple workers)
- Health check endpoint for Railway monitoring

### Frontend
- Pure static files (no build process)
- API URL configured via env.js
- Client-side routing via URL parameters
- All API calls use fetch with error handling
- Charts rendered client-side with Chart.js

### Data
- Read-only JSON files
- Index file cached in memory
- Citation index built on startup
- Word cloud exclusions from user memory [[memory:8559522]]

### Deployment
- Railway auto-detects Python app
- Vercel serves static files via CDN
- Both support automatic deployments
- Environment variables set via platform dashboards

## Word Cloud Exclusions
Always exclude these words from word cloud analyses [[memory:8559522]]:
- details, page, https, filevineapp, docviewer, view, source, embedding
- Common English words (the, and, or, of, to, in, a, is, etc.)

## Development Best Practices

1. **Backend changes** → Test locally → Update API docs → Commit
2. **Frontend changes** → Test with local backend → Verify API calls → Commit
3. **New features** → Update all documentation files
4. **Bug fixes** → Test thoroughly → Document in commit message
5. **API changes** → Update both backend and frontend API client
6. **Environment changes** → Update deployment guides

## Testing Strategy

### Local Testing
1. Start backend: `cd backend && python app.py`
2. Verify health check: `curl http://localhost:5000/health`
3. Start frontend: `cd frontend && python -m http.server 8080`
4. Visit `http://localhost:8080`
5. Test all features

### Pre-deployment Testing
1. Backend responds to all API endpoints
2. CORS headers configured correctly
3. Frontend connects to backend
4. All features work end-to-end
5. No console errors

## Troubleshooting Common Issues

### CORS Errors
- Verify CORS_ORIGINS matches Vercel URL exactly
- No trailing slashes
- Restart Railway after env var changes

### API Connection Issues
- Check env.js has correct Railway URL
- Verify Railway backend is running (/health)
- Check browser console for errors

### Data Not Loading
- Verify data directory path
- Check symlink exists: `ls -la backend/data`
- Ensure index.json is readable

## Future Enhancements
- User authentication
- Advanced search (fuzzy, regex)
- Favorites/bookmarks
- Case comparison
- Export functionality
- Rate limiting
- GraphQL API
- Mobile app

---

This architecture supports scaling to 8.5M+ cases with proper indexing and caching strategies.

