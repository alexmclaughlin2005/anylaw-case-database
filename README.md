# AnyLaw Case Database Navigator

A web application for browsing, searching, and analyzing the Lexsphere caselaw database containing 8.5M+ U.S. judicial opinions.

![Dashboard](https://img.shields.io/badge/Status-Active-success)
![Flask](https://img.shields.io/badge/Flask-3.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## 📚 Overview

The AnyLaw Case Database Navigator provides an intuitive interface to explore a comprehensive legal database including:

- **8.5M+ cases** from 200+ jurisdictions
- **U.S. Supreme Court** opinions (since 1882)
- **Federal Circuit Courts** across all circuits
- **Federal District Courts** nationwide
- **State Supreme and Appellate Courts** (all 50 states)
- **Bankruptcy and Tribal Courts**

### Data Source

This application uses data from **Lexsphere**, a proprietary database of U.S. judicial opinions with:
- Full-text appellate decisions
- Citations and references
- Structured metadata (jurisdiction, docket numbers, dates)
- Attorney and judge information
- Case categorization

## 🚀 Features

### 📊 Dashboard
- **Real-time Statistics**: Total cases, jurisdictions, date ranges
- **Interactive Charts**: Visualize case distribution by jurisdiction and year
- **Quick Navigation**: Jump to search or explore specific features

### 🔍 Search & Filter
- **Text Search**: Find cases by title, keywords, or jurisdiction
- **Advanced Filters**: Filter by jurisdiction and year
- **Pagination**: Browse through large result sets
- **Quick Preview**: See key metadata before opening full case

### 📄 Case Detail Viewer
- **Full Metadata**: Jurisdiction, date, docket number, citations
- **Legal Information**: Judges, attorneys, case categories
- **Full Opinion Text**: Complete case body with on-demand loading
- **Smart Display**: Hide/show sections based on available data

### 📈 Data Visualization
- **Jurisdiction Analysis**: Bar charts showing case distribution
- **Temporal Trends**: Line charts tracking cases over time
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or navigate to the project directory:**
```bash
cd "/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw"
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify data files exist:**
Ensure the `Anylaw sample documents-b/` directory contains:
- `index.json` (master index)
- `doc_*.json` files (individual cases)

4. **Run the application:**
```bash
python app.py
```

5. **Access the application:**
Open your web browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### Viewing Dashboard

1. Open the homepage to see database statistics
2. Explore interactive charts showing:
   - Top jurisdictions by case count
   - Cases published over time
3. Review database information and coverage

### Searching Cases

1. Click **"Search Cases"** in the navigation menu
2. Choose your search mode:
   
   **Text Search Tab:**
   - Enter search terms in the search box:
     - Case titles (e.g., "Brown v. Board")
     - Keywords (e.g., "constitutional")
     - Jurisdiction names
   - Apply filters:
     - **Jurisdiction**: Select from dropdown
     - **Year**: Enter specific year (e.g., 2020)
   
   **Citation Lookup Tab:**
   - Enter a legal citation (e.g., "367 U.S. 1", "251 F. Supp.2d 176")
   - Click "Find Case" to jump directly to that case
   - Perfect when you have the exact citation reference
   
3. Browse results and click any case to view details
4. Use pagination to navigate through results (text search)

### Viewing Case Details

1. Click on any case from search results
2. Review case metadata:
   - Full case title and caption
   - Jurisdiction and court
   - Opinion date
   - Docket number
   - **Legal citations (clickable!)**
3. View case information:
   - Judges presiding
   - Attorneys representing parties
   - Case categories/topics
4. Click **"Show Full Text"** to read the complete opinion

### Cross-Referencing Cases (NEW!)

1. On any case detail page, look at the **Citations** section
2. **Click any citation badge** (they're now interactive!)
3. If the cited case is in the database:
   - ✓ You'll be redirected to that case automatically
4. If not in your sample:
   - ℹ️ You'll see a helpful message
5. **Navigate between related cases** by following citation links

## 🏗️ Project Structure

```
AnyLaw/
├── app.py                          # Flask application (backend)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── AI_Instructions.md              # Detailed technical docs
├── AI_System_Prompt.md            # High-level architecture
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base layout
│   ├── index.html                 # Dashboard
│   ├── search.html                # Search page
│   └── case.html                  # Case detail page
│
├── static/                        # Static assets
│   ├── css/
│   │   └── style.css             # Styles
│   └── js/
│       └── main.js               # JavaScript utilities
│
└── Anylaw sample documents-b/     # Data files
    ├── index.json                # Master index (1.5MB)
    └── doc_*.json                # Case documents (1000 files)
```

## 🔧 Technical Details

### Technology Stack

- **Backend**: Flask 3.0.0 (Python web framework)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Visualization**: Chart.js 4.4.0
- **Data Format**: JSON

### API Endpoints

The application provides RESTful API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stats` | GET | Database statistics |
| `/api/jurisdictions` | GET | List of jurisdictions |
| `/api/search` | GET | Search cases with filters |
| `/api/document/<id>` | GET | Get full case document |

### Data Structure

Each case document contains:
- **Metadata**: Title, jurisdiction, date, docket
- **Full Opinion**: Complete case text
- **Citations**: Legal citations (e.g., "251 F. Supp.2d 176")
- **Parties**: Attorneys and judges
- **Categories**: Legal topics and classifications

## 🎨 Customization

### Modifying Styles

Edit `static/css/style.css` to customize:
- Color scheme (CSS variables at top of file)
- Layout and spacing
- Responsive breakpoints
- Component styles

### Adding Features

See `AI_Instructions.md` for detailed guidance on:
- Adding new API endpoints
- Creating new pages
- Implementing new searches
- Extending data models

## 🐛 Troubleshooting

### Application won't start

**Problem**: Port 5000 already in use
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### No data showing

**Problem**: Index file not found
**Solution**: Verify `Anylaw sample documents-b/index.json` exists and is valid JSON

### Charts not rendering

**Problem**: Chart.js not loading
**Solution**: Check internet connection (CDN resource) or serve Chart.js locally

### Search returns no results

**Problem**: Filters too restrictive
**Solution**: Clear filters and try broader search terms

## 📊 Database Coverage

### Federal Courts
- U.S. Supreme Court (1882-present)
- 13 Circuit Courts of Appeals (1930-present)
- 94 District Courts (various start dates)
- Federal Circuit Court (1982-present)

### State Courts
- All 50 state supreme courts
- State appellate courts
- Varying coverage dates by state (earliest: 1848)

### Special Courts
- Bankruptcy Courts
- Tribal Courts
- Washington D.C. Courts

## 🔒 Data Privacy

This application:
- Reads data locally (no external API calls for data)
- Does not modify original data files
- Contains only public judicial opinions
- Does not track or store user searches

## 📝 License

This application is provided for analysis and research of the Lexsphere caselaw database sample. The underlying data is proprietary to Lexsphere.

## 🤝 Contributing

For technical documentation and development guidelines, see:
- `AI_Instructions.md` - Detailed technical documentation
- `AI_System_Prompt.md` - Architecture overview

## 📞 Support

For questions about:
- **The Application**: Review `AI_Instructions.md` for technical details
- **The Data**: Contact Lexsphere regarding their database
- **Setup Issues**: Check the Troubleshooting section above

## 🎯 Use Cases

This application supports:
- **Legal Research**: Find and analyze case law
- **Academic Study**: Research legal trends and patterns
- **AI Training**: Prepare data for legal AI models
- **Database Evaluation**: Assess Lexsphere data quality and coverage
- **Compliance**: Analyze jurisdictional coverage for compliance tools

## 📈 Future Enhancements

Potential features for future development:
- Full-text search with Elasticsearch
- Advanced filtering (by attorney, judge, citation count)
- Case comparison tool
- Citation network visualization
- Export to PDF/CSV
- Bookmark favorite cases
- Search history
- User authentication

---

**Version**: 1.0.0  
**Last Updated**: December 17, 2025  
**Author**: Built with AI assistance for AnyLaw project

