# AnyLaw Case Database Navigator - AI System Prompt

## Project Overview
AnyLaw Case Database Navigator is a web application for browsing, searching, and analyzing the Lexsphere caselaw database. The application provides a user-friendly interface to explore 8.5M+ U.S. judicial opinions across 200+ jurisdictions.

## High-Level Architecture

### Backend (Flask)
- **app.py** - Main Flask application with API endpoints and routing
- **CaseLawDatabase class** - Data access layer for indexing and searching cases

### Frontend (HTML/CSS/JavaScript)
- **templates/** - Jinja2 HTML templates for all pages
- **static/css/** - Stylesheets for UI components
- **static/js/** - Client-side JavaScript utilities and API client

### Data
- **Anylaw sample documents-b/** - JSON files containing case data and metadata
- **index.json** - Master index of all documents with summary metadata

## Directory Structure

```
/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw/
├── app.py                          # Main Flask application
├── templates/                      # HTML templates
│   ├── base.html                  # Base template with navigation
│   ├── index.html                 # Dashboard/home page
│   ├── search.html                # Search interface
│   └── case.html                  # Case detail viewer
├── static/                        # Static assets
│   ├── css/
│   │   └── style.css             # Main stylesheet
│   └── js/
│       └── main.js               # JavaScript utilities and API client
├── Anylaw sample documents-b/     # Case data (1000+ JSON files)
│   ├── index.json                # Master index
│   └── doc_*.json                # Individual case documents
├── requirements.txt               # Python dependencies
├── README.md                      # User documentation
├── AI_Instructions.md             # Detailed technical documentation
└── AI_System_Prompt.md           # This file - high-level overview
```

## Key Features

1. **Dashboard** - Statistics and visualizations of the database
2. **Search** - Filter and search cases by jurisdiction, year, keywords
3. **Case Detail Viewer** - View full case information including opinions
4. **Data Visualization** - Charts showing distribution by jurisdiction and year

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Visualization**: Chart.js
- **Data Format**: JSON

## Maintenance Instructions

### Creating/Updating Documentation Files

When modifying this project, always maintain:

1. **AI_System_Prompt.md** (this file)
   - High-level overview of the app
   - Directory structure
   - Key features and architecture
   - Update when: adding major features, changing architecture

2. **AI_Instructions.md**
   - Detailed technical documentation
   - API endpoints and data models
   - Component descriptions
   - Code examples and patterns
   - Update when: adding/modifying any code, changing data structures

3. **README.md**
   - User-facing documentation
   - Installation and setup instructions
   - Usage guide
   - Update when: changing setup process or user workflows

### File Purposes

- **app.py** - Flask application, routes, and business logic
- **templates/base.html** - Shared layout, navigation, footer
- **templates/index.html** - Dashboard with stats and charts
- **templates/search.html** - Search interface with filters
- **templates/case.html** - Individual case detail page
- **static/css/style.css** - All styles and responsive design
- **static/js/main.js** - API client and utility functions
- **requirements.txt** - Python package dependencies
- **Anylaw sample documents-b/** - Raw data files (read-only)

## Development Workflow

1. Backend changes → Update `app.py`
2. Frontend UI → Update templates and CSS
3. API changes → Update both backend and frontend API client
4. New features → Update all three documentation files
5. Dependencies → Update `requirements.txt`

## Important Notes

- The database is read-only (files in `Anylaw sample documents-b/`)
- Word cloud exclusions list is defined in `app.py` (from user memory)
- All dates should be formatted consistently using ISO format
- Case bodies are very large (100KB+) - lazy load when needed
- Search is currently simple text matching (can be enhanced with full-text search)

