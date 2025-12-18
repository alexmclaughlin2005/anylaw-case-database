# AnyLaw Case Database Navigator - Detailed Technical Documentation

## Table of Contents
1. [Data Structure](#data-structure)
2. [Backend Architecture](#backend-architecture)
3. [API Endpoints](#api-endpoints)
4. [Frontend Components](#frontend-components)
5. [Services and Utilities](#services-and-utilities)
6. [File Reference](#file-reference)

## Data Structure

### Source Data: Lexsphere Case Database

Located in: `/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw/Anylaw sample documents-b/`

#### index.json
Contains an array of document summaries (1000 cases in sample):

```json
{
  "documents": [
    {
      "id": "unique_id",
      "filename": "doc_0001_ID.json",
      "title": "Case Title",
      "jurisdiction": "Court/Jurisdiction Name",
      "date": "2003-05-01T00:00:00.000Z",
      "body_length": 2755476,
      "cited_as": ["251 F. Supp.2d 176"],
      "attorneys": "Attorney names...",
      "judges": "Judge names..."
    }
  ]
}
```

#### Individual Case Files (doc_*.json)
Each file contains full case data:

```json
{
  "id": "unique_id",
  "document": {
    "title": "Short case title",
    "full_title": "Full case caption",
    "jurisdiction": "Court name",
    "date": "ISO date string",
    "docket": "Docket number",
    "body": "Full opinion text (very large, 100KB+)",
    "body_length": 142984,
    "citedas": ["citation1", "citation2"],
    "attorneys": "Attorney listing text",
    "category": ["category1", "category2"],
    "judges": "Judge names and roles",
    "citation_count": 5
  }
}
```

**Key Fields:**
- `id` - Unique case identifier (used for lookups)
- `title` - Short case name (e.g., "Smith v. Jones")
- `full_title` - Complete case caption
- `jurisdiction` - Court that issued the opinion
- `date` - Opinion date in ISO 8601 format
- `body` - Full case text (can be 100KB+)
- `body_length` - Size of body in bytes
- `citedas` - Array of legal citations
- `category` - Array of legal categories/topics
- `citation_count` - Number of times cited

## Backend Architecture

### app.py - Flask Application

#### Configuration
```python
DATA_DIR = Path(__file__).parent / "Anylaw sample documents-b"
INDEX_FILE = DATA_DIR / "index.json"
EXCLUDED_WORDS = {'details', 'page', 'https', ...}  # Word cloud exclusions
```

#### CaseLawDatabase Class

**Purpose**: Manages all database operations with caching

**Key Methods:**

1. **`index` (property)**
   - Lazy loads the index.json file
   - Caches in memory for performance
   - Returns: List of document summaries

2. **`get_stats()`**
   - Calculates database statistics
   - Aggregates: jurisdictions, years, citations, body lengths
   - Caches results
   - Returns: Statistics dictionary

3. **`search(query, jurisdiction, year, limit, offset)`**
   - Filters cases by multiple criteria
   - Simple text matching in title/jurisdiction/full_title
   - Pagination support
   - Returns: Dictionary with results array and metadata

4. **`get_document(doc_id)`**
   - Loads full document from individual JSON file
   - Finds filename from index
   - Returns: Complete document object

5. **`get_jurisdictions()`**
   - Extracts unique jurisdiction list
   - Sorted alphabetically
   - Returns: List of jurisdiction names

### Routes and Endpoints

#### Page Routes (HTML)
- `GET /` → `index.html` - Dashboard
- `GET /search` → `search.html` - Search page
- `GET /case/<doc_id>` → `case.html` - Case detail

#### API Routes (JSON)
- `GET /api/stats` → Database statistics
- `GET /api/jurisdictions` → List of jurisdictions
- `GET /api/search?q=&jurisdiction=&year=&limit=&offset=` → Search results
- `GET /api/document/<doc_id>` → Full document

## API Endpoints

### GET /api/stats
Returns database statistics.

**Response:**
```json
{
  "total_cases": 1000,
  "jurisdictions": {
    "Supreme Court": 50,
    "Ninth Circuit": 120
  },
  "years": {
    "2020": 45,
    "2021": 52
  },
  "avg_body_length": 145000,
  "total_citations": 2500,
  "date_range": {
    "earliest": 1882,
    "latest": 2023
  }
}
```

### GET /api/jurisdictions
Returns sorted list of all jurisdictions.

**Response:**
```json
["Fifth Circuit", "Ninth Circuit", "Supreme Court of Connecticut", ...]
```

### GET /api/search
Search and filter cases.

**Query Parameters:**
- `q` (string) - Search query (matches title, jurisdiction, full_title)
- `jurisdiction` (string) - Filter by exact jurisdiction name
- `year` (string) - Filter by year (e.g., "2020")
- `limit` (int) - Results per page (default: 50)
- `offset` (int) - Starting position (default: 0)

**Response:**
```json
{
  "results": [
    {
      "id": "doc_id",
      "title": "Case Title",
      "jurisdiction": "Court",
      "date": "2020-01-01T00:00:00.000Z",
      "cited_as": ["123 F.3d 456"]
    }
  ],
  "total": 150,
  "limit": 20,
  "offset": 0
}
```

### GET /api/document/<doc_id>
Get full document by ID.

**Response:** Full document object (see Data Structure above)

**Error Response (404):**
```json
{
  "error": "Document not found"
}
```

## Frontend Components

### templates/base.html
Base template with shared layout.

**Blocks:**
- `{% block title %}` - Page title
- `{% block extra_head %}` - Additional head content
- `{% block content %}` - Main page content
- `{% block extra_scripts %}` - Page-specific JavaScript

**Features:**
- Navigation bar with links
- Footer with database info
- Loads Chart.js library
- Includes main.css and main.js

### templates/index.html
Dashboard with statistics and visualizations.

**Components:**
1. Page header
2. Stats grid (4 stat cards)
3. Charts grid (jurisdictions bar chart, years line chart)
4. Action cards (links to search, etc.)
5. Info section (database overview)

**JavaScript Functions:**
- `loadStats()` - Fetches and displays statistics
- `displayStats()` - Updates stat cards
- `createCharts()` - Initializes Chart.js visualizations

**Charts:**
- Jurisdictions: Bar chart (top 10 jurisdictions)
- Years: Line chart (last 30 years)

### templates/search.html
Search interface with filters and results.

**Components:**
1. Search tabs (Text Search / Citation Lookup)
2. Text search box (input + button)
3. Citation lookup box (input + button)
4. Filter controls (jurisdiction dropdown, year input)
5. Results info (count display)
6. Results container (case cards)
7. Pagination controls

**JavaScript Functions:**
- `switchTab(mode)` - Switches between text search and citation lookup
- `lookupByCitation()` - Finds case by citation string
- `loadJurisdictions()` - Populates jurisdiction dropdown
- `performSearch(page)` - Executes search with current filters
- `displayResults(results)` - Renders result cards
- `displayPagination(total, offset)` - Creates page buttons
- `clearFilters()` - Resets all filters
- `formatDate(dateStr)` - Formats dates for display
- `escapeHtml(text)` - Prevents XSS

**Search Features:**
- **Two search modes**: Text search and Citation lookup (tabbed interface)
- Text search: search by title, keywords, jurisdiction
- Citation lookup: find exact case by citation (e.g., "367 U.S. 1")
- Jurisdiction filtering (text search only)
- Year filtering (text search only)
- Pagination (20 results per page)
- Enter key support for both modes

### templates/case.html
Detailed case viewer.

**Components:**
1. Breadcrumb navigation
2. Case header (title + metadata grid)
3. Citations section
4. Categories (tags)
5. Judges section
6. Attorneys section
7. Full opinion (expandable)

**JavaScript Functions:**
- `loadCase()` - Fetches case by ID from URL
- `displayCase()` - Populates all sections
- `toggleBody()` - Show/hide full opinion text
- `formatDate(dateStr)` - Format date
- `estimateWords(bytes)` - Calculate word count
- `escapeHtml(text)` - Prevent XSS

**Features:**
- Lazy loading of full opinion text (can be 100KB+)
- Word count estimation
- Conditional section display (hide if no data)
- Error handling for missing cases

### static/css/style.css
Complete stylesheet for the application.

**CSS Variables:**
```css
--primary-color: #2563eb (blue)
--secondary-color: #64748b (gray)
--success-color: #10b981 (green)
--danger-color: #ef4444 (red)
--bg-color: #f8fafc (light gray)
--card-bg: #ffffff (white)
--text-color: #1e293b (dark)
--text-light: #64748b (light gray)
--border-color: #e2e8f0
--shadow: subtle shadow
--shadow-lg: prominent shadow
```

**Key Classes:**
- `.container` - Max-width content wrapper
- `.navbar` - Sticky navigation bar
- `.stats-grid` - Responsive grid for stat cards
- `.stat-card` - Individual statistic display
- `.chart-card` - Chart container
- `.search-box` - Search input + button
- `.result-card` - Search result item
- `.case-header` - Case detail header
- `.section` - Content section card
- `.btn-primary`, `.btn-secondary` - Button styles

**Responsive Design:**
- Mobile-first approach
- Breakpoint at 768px
- Flexible grids (auto-fit, minmax)
- Collapsible layouts on small screens

### static/js/main.js
Client-side utilities and API client.

**Utilities Object:**
```javascript
utils = {
  formatDate(dateStr)    // ISO date → readable format
  escapeHtml(text)       // XSS prevention
  formatNumber(num)      // Add thousand separators
  estimateWords(bytes)   // Byte count → word estimate
  formatBytes(bytes)     // Bytes → KB/MB
  debounce(func, wait)   // Debounce for search
}
```

**API Client:**
```javascript
api = {
  getStats()                    // Fetch /api/stats
  search(query, filters)        // Fetch /api/search
  getDocument(docId)            // Fetch /api/document/:id
  getJurisdictions()            // Fetch /api/jurisdictions
}
```

All API methods return Promises and handle errors.

## Services and Utilities

### Data Loading
1. **Index Loading**: Lazy loads index.json on first access
2. **Document Loading**: Reads individual files on demand
3. **Caching**: Statistics cached in memory after first calculation

### Search Algorithm
Current implementation uses simple string matching:
- Converts query and fields to lowercase
- Checks if query appears in title, jurisdiction, or full_title
- Future enhancement: Full-text search with Elasticsearch

### Performance Considerations
- Index cached in memory (prevents repeated file reads)
- Stats calculated once and cached
- Full case bodies only loaded when requested
- Pagination limits results transferred

## File Reference

### Backend Files

**app.py** (200+ lines)
- Flask application and routing
- CaseLawDatabase class
- API endpoint handlers
- Configuration and startup

### Frontend Files

**templates/base.html** (40 lines)
- Base template structure
- Navigation and footer
- Script/style includes

**templates/index.html** (120 lines)
- Dashboard layout
- Statistics display
- Chart initialization
- Info cards

**templates/search.html** (150 lines)
- Search interface
- Filter controls
- Results display
- Pagination logic

**templates/case.html** (140 lines)
- Case detail layout
- Metadata display
- Full text viewer
- Section visibility logic

**static/css/style.css** (600+ lines)
- Complete application styles
- Responsive design
- Component classes
- Utility classes

**static/js/main.js** (100 lines)
- Utility functions
- API client
- Reusable helpers

### Data Files

**Anylaw sample documents-b/index.json** (1.5MB)
- Master index of 1000 cases
- Summary metadata for each case

**Anylaw sample documents-b/doc_*.json** (100-150KB each)
- Individual case files
- Full opinion text and metadata
- 1000 total files in sample

### Documentation Files

**README.md**
- User-facing documentation
- Installation instructions
- Usage guide

**AI_Instructions.md** (this file)
- Technical documentation
- API reference
- Code patterns and examples

**AI_System_Prompt.md**
- High-level overview
- Directory structure
- Maintenance guidelines

**requirements.txt**
- Python dependencies
- Flask and related packages

## Code Patterns

### Adding a New API Endpoint

1. Add route to app.py:
```python
@app.route('/api/newfeature')
def api_new_feature():
    data = db.some_method()
    return jsonify(data)
```

2. Add method to CaseLawDatabase class if needed

3. Update API client in main.js:
```javascript
api.newFeature = async () => {
  const response = await fetch(`${api.baseUrl}/api/newfeature`);
  if (!response.ok) throw new Error('Failed');
  return await response.json();
}
```

4. Use in frontend:
```javascript
const data = await api.newFeature();
```

### Adding a New Page

1. Create template in templates/:
```html
{% extends "base.html" %}
{% block title %}New Page{% endblock %}
{% block content %}
  <!-- Content here -->
{% endblock %}
```

2. Add route in app.py:
```python
@app.route('/newpage')
def new_page():
    return render_template('newpage.html')
```

3. Add navigation link in base.html

### Styling Patterns

Use existing CSS classes:
- Cards: `.stat-card`, `.chart-card`, `.result-card`
- Buttons: `.btn-primary`, `.btn-secondary`
- Layout: `.container`, `.section`
- Grid: `.stats-grid`, `.charts-grid`

## Memory and Configuration

### Word Cloud Exclusions
Defined in `app.py` as `EXCLUDED_WORDS`:
```python
EXCLUDED_WORDS = {'details', 'page', 'https', 'filevineapp', 
                  'docviewer', 'view', 'source', 'embedding',
                  'the', 'and', 'or', 'of', 'to', 'in', 'a', 
                  'is', 'that', 'for', 'with', 'as', 'on'}
```

This list should be used for any word frequency analysis or word cloud generation.

## Development Notes

### Running the Application
```bash
cd /Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw
python app.py
```

Access at: http://localhost:5000

### Modifying Data Structure
If Lexsphere changes their data format:
1. Update data models in this documentation
2. Update CaseLawDatabase methods in app.py
3. Test all API endpoints
4. Update frontend display logic if needed

### Future Enhancements
- Full-text search (Elasticsearch integration)
- Advanced filtering (by attorney, judge, citation count)
- Export functionality (PDF, CSV)
- Case comparison tool
- Citation network visualization
- Bookmark/favorite cases
- Search history
- API rate limiting
- User authentication (if needed)

## Testing Checklist

When making changes, verify:
- [ ] Dashboard loads and displays stats
- [ ] Charts render correctly
- [ ] Search returns relevant results
- [ ] Filters work (jurisdiction, year)
- [ ] Pagination works
- [ ] Case detail page loads
- [ ] All metadata displays properly
- [ ] Full opinion text shows/hides
- [ ] Mobile responsive design works
- [ ] No console errors
- [ ] API endpoints return correct data
- [ ] Error handling works (missing cases, network errors)

