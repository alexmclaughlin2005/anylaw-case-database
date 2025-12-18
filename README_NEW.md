# AnyLaw Case Database Navigator

A modern web application for browsing, searching, and analyzing the Lexsphere caselaw database containing 8.5M+ U.S. judicial opinions.

## 🏗️ Architecture

This application uses a separated architecture optimized for cloud deployment:

- **Frontend**: Static HTML/CSS/JavaScript hosted on Vercel
- **Backend**: Flask REST API hosted on Railway
- **Data**: JSON-based caselaw database

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│   Vercel        │         │    Railway       │         │    Data     │
│   (Frontend)    │────────▶│   (Backend API)  │────────▶│  JSON Files │
│   Static Site   │  HTTP   │   Flask + CORS   │  Read   │  8.5M cases │
└─────────────────┘         └──────────────────┘         └─────────────┘
```

## 🚀 Quick Start

### Local Development

#### Backend (Terminal 1)

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend
python app.py
```

Backend will be available at `http://localhost:5000`

Test it: Visit `http://localhost:5000/health`

#### Frontend (Terminal 2)

```bash
cd frontend

# Serve static files (Python)
python3 -m http.server 8080

# OR use any static server:
# npx serve
# php -S localhost:8080
```

Frontend will be available at `http://localhost:8080`

Visit `http://localhost:8080` to see the application.

## 📁 Project Structure

```
AnyLaw/
├── backend/                    # Flask API (Railway)
│   ├── app.py                 # Main API application
│   ├── requirements.txt       # Python dependencies
│   ├── Procfile              # Railway start command
│   ├── runtime.txt           # Python version
│   ├── railway.json          # Railway config
│   └── data/                 # Symlink to case data
│
├── frontend/                  # Static site (Vercel)
│   ├── index.html            # Dashboard
│   ├── search.html           # Search interface
│   ├── case.html             # Case detail viewer
│   ├── env.js                # Environment config
│   ├── vercel.json           # Vercel config
│   └── static/
│       ├── css/
│       │   └── style.css     # Styles
│       └── js/
│           ├── api.js        # API client
│           └── main.js       # Utilities
│
├── Anylaw sample documents-b/ # Case data (1000+ JSON files)
│   ├── index.json            # Master index
│   └── doc_*.json            # Individual cases
│
├── DEPLOYMENT_PLAN.md        # Detailed deployment plan
├── GITLAB_DEPLOYMENT_GUIDE.md # GitLab/Railway/Vercel guide
└── README.md                 # This file
```

## 🎯 Features

### Dashboard
- Real-time database statistics
- Interactive charts (jurisdictions, years)
- Quick action cards
- Database overview

### Search
- **Text Search**: Search by case title, keywords, jurisdiction
- **Citation Lookup**: Find cases by legal citation (e.g., "367 U.S. 1")
- **Filters**: Jurisdiction and year filters
- **Pagination**: Browse through results

### Case Detail
- Full case information
- Citation references
- Extracted citations (cases cited in opinion)
- Clickable citation navigation
- Categories, judges, attorneys
- Full opinion text (expandable)

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0
- **CORS**: flask-cors
- **Server**: Gunicorn (production)
- **Language**: Python 3.11

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **JavaScript**: Vanilla JS (no framework dependencies)
- **Charts**: Chart.js for visualizations
- **API Client**: Custom fetch-based client

### Deployment
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Railway
- **Version Control**: GitLab
- **CI/CD**: Automatic deployment on push

## 🌐 API Endpoints

All endpoints are under `/api/`:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/stats` | GET | Database statistics |
| `/api/jurisdictions` | GET | List of jurisdictions |
| `/api/search?q=&jurisdiction=&year=` | GET | Search cases |
| `/api/document/<id>` | GET | Get full document |
| `/api/citation/<citation>` | GET | Find by citation |
| `/api/citations?limit=100` | GET | List all citations |

### Example API Calls

```bash
# Get stats
curl https://your-backend.railway.app/api/stats

# Search
curl https://your-backend.railway.app/api/search?q=brown&jurisdiction=US

# Get document
curl https://your-backend.railway.app/api/document/H42GQWYBTlTomsSBT--K

# Find by citation
curl https://your-backend.railway.app/api/citation/367%20U.S.%201
```

## 📊 Database Overview

- **Total Cases**: 8.5M+ U.S. judicial opinions
- **Jurisdictions**: 200+ (Federal and State courts)
- **Date Range**: 1882 - Present
- **Citations**: 1,925 unique legal citations
- **Format**: JSON with full text and structured metadata

### Coverage
- U.S. Supreme Court (since 1882)
- Federal Circuit Courts
- Federal District Courts
- State Supreme and Appellate Courts
- Bankruptcy and Tribal Courts

## 🚢 Deployment

See detailed guides:
- **[Deployment Plan](DEPLOYMENT_PLAN.md)**: Complete architecture and implementation plan
- **[GitLab Deployment Guide](GITLAB_DEPLOYMENT_GUIDE.md)**: Step-by-step GitLab, Railway, and Vercel setup

### Quick Deployment Steps

1. **Push to GitLab**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://gitlab.com/username/anylaw.git
   git push -u origin main
   ```

2. **Deploy Backend to Railway**
   - Connect GitLab repository
   - Set root directory: `backend`
   - Add environment variables
   - Deploy

3. **Deploy Frontend to Vercel**
   - Connect GitLab repository
   - Set root directory: `frontend`
   - Add API_URL environment variable
   - Deploy

## 🔧 Configuration

### Backend Environment Variables

```bash
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend.vercel.app
DATA_DIR=/app/data
PORT=8000
```

### Frontend Environment Variables

```bash
API_URL=https://your-backend.railway.app
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
python app.py

# In another terminal
curl http://localhost:5000/health
curl http://localhost:5000/api/stats
```

### Frontend Tests

1. Start backend (see above)
2. Serve frontend: `cd frontend && python3 -m http.server 8080`
3. Visit `http://localhost:8080`
4. Test all features:
   - Dashboard loads with stats
   - Search works
   - Citation lookup works
   - Case detail page loads
   - Navigation works

## 🔐 Security

- CORS configured for specific origins
- Input sanitization in frontend
- XSS protection headers
- No sensitive data exposure
- HTTPS enforced in production

## 📈 Performance

- Lazy loading of case bodies
- Index caching in backend
- Efficient pagination
- CDN-served static assets (Vercel)
- Optimized JSON parsing

## 🤝 Contributing

This is a personal project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project uses the Lexsphere caselaw database. Please review the data license before use.

## 🆘 Support & Troubleshooting

### Common Issues

**CORS Errors**
- Check CORS_ORIGINS matches your frontend URL
- No trailing slashes in URLs
- Restart backend after changes

**API Connection Failed**
- Verify backend is running
- Check env.js has correct API URL
- Verify Railway backend is deployed

**Case Not Loading**
- Check document ID is correct
- Verify data files are accessible
- Check browser console for errors

### Getting Help

- Check the deployment guides
- Review Railway/Vercel logs
- Open an issue on GitLab

## 🎯 Roadmap

- [ ] Add user authentication
- [ ] Implement advanced search (fuzzy matching, regex)
- [ ] Add favorites/bookmarks
- [ ] Case comparison tool
- [ ] Export functionality (PDF, citations)
- [ ] API rate limiting
- [ ] GraphQL API option
- [ ] Mobile app version

## 👥 Credits

- **Dataset**: Lexsphere caselaw database
- **Charts**: Chart.js
- **Deployment**: Railway and Vercel

---

Built with ❤️ for legal research and AI training applications.

