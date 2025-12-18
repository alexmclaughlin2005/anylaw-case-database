# AnyLaw Database Navigator - Quick Start Guide

## 🚀 Get Started in 30 Seconds

### 1. Open Terminal
```bash
cd "/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw"
```

### 2. Run the App
```bash
./start.sh
```
OR
```bash
python3 app.py
```

### 3. Open Browser
Navigate to: **http://localhost:5000**

That's it! 🎉

---

## 📱 What You'll See

### Dashboard (Home Page)
- Database statistics (total cases, jurisdictions, date ranges)
- Interactive charts showing case distribution
- Quick links to search and explore

### Search Page
- Text search box (try: "constitutional", "Brown", "Miranda")
- Filter by jurisdiction (dropdown)
- Filter by year (e.g., 2020, 1954)
- Results with pagination (20 per page)

### Case Detail Page
- Full case information
- Metadata (date, jurisdiction, citations)
- Judges and attorneys
- Click "Show Full Text" to read complete opinion

---

## 🔍 Quick Examples

### Search for Famous Cases
1. Go to Search page
2. Type: "Brown v. Board" or "Miranda" or "Roe"
3. Click Search
4. Click any result to view full case

### Filter by Jurisdiction
1. Go to Search page
2. Select a jurisdiction from dropdown (e.g., "Supreme Court")
3. Click Search
4. Browse cases from that court

### Browse by Year
1. Go to Search page
2. Enter year in Year filter (e.g., "2020")
3. Click Search
4. See all cases from that year

---

## 📚 Sample Database

### What's Included
- **1,000 cases** (sample from 8.5M+ full database)
- **Federal courts**: Supreme Court, Circuit Courts, District Courts
- **State courts**: All 50 states' supreme and appellate courts
- **Date range**: 1882-2023
- **Full text**: Complete opinions with metadata

### Data Location
```
Anylaw sample documents-b/
├── index.json (master index - 1.5MB)
└── doc_*.json (1000 case files - 100-150KB each)
```

---

## 🛠️ Troubleshooting

### Port Already in Use?
Edit `app.py` line 175:
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```

### Missing Dependencies?
```bash
pip install -r requirements.txt
```

### Can't Find Data?
Verify the folder `Anylaw sample documents-b` exists in the project directory.

---

## 📖 Need More Help?

### Documentation Files
- **README.md** - Complete user guide
- **AI_Instructions.md** - Technical documentation
- **AI_System_Prompt.md** - Architecture overview
- **PROJECT_SUMMARY.md** - Project overview

### Key Shortcuts
- **Home**: Click "AnyLaw Database Navigator" logo
- **Search**: Click "Search Cases" in navigation
- **Back**: Use browser back button or breadcrumbs

---

## 🎯 Common Tasks

### Finding a Specific Case
1. Know the case name? Use search box
2. Know the jurisdiction? Use jurisdiction filter
3. Know the year? Use year filter
4. Combine filters for precise results

### Exploring the Database
1. Start at Dashboard to see statistics
2. Use charts to identify interesting jurisdictions/years
3. Go to Search and filter by what you found
4. Browse through results

### Reading a Full Case
1. Search or browse to find case
2. Click case title
3. Scroll through metadata sections
4. Click "Show Full Text" button
5. Scroll through complete opinion

---

## ⚡ Pro Tips

1. **Clear Filters**: Click "Clear Filters" to reset search
2. **Pagination**: Use page numbers at bottom to browse more results
3. **Performance**: Case bodies are large - they load on demand when you click "Show Full Text"
4. **Charts**: Hover over chart elements to see exact numbers
5. **Navigation**: Use breadcrumbs on case detail page to go back

---

## 🎨 Customization

### Change Colors
Edit `static/css/style.css` - lines 3-14 (CSS variables)

### Change Results Per Page
Edit `templates/search.html` - line 88 (`resultsPerPage = 20`)

### Change Port
Edit `app.py` - line 175 (`port=5000`)

---

## 📊 At a Glance

| Feature | Location | Action |
|---------|----------|--------|
| View Stats | Dashboard (/) | Load homepage |
| Search Cases | Search Page (/search) | Click "Search Cases" |
| View Case | Case Detail (/case/ID) | Click any case title |
| Filter Results | Search Page | Use dropdowns/inputs |
| Read Opinion | Case Detail | Click "Show Full Text" |

---

## ✅ Quick Validation

Test that everything works:

```bash
# Validate setup
python3 -c "
import json
from pathlib import Path
assert Path('Anylaw sample documents-b/index.json').exists()
with open('Anylaw sample documents-b/index.json') as f:
    data = json.load(f)
    assert len(data['documents']) == 1000
print('✅ All systems ready!')
"
```

---

## 🚦 Stop the Server

Press `Ctrl + C` in the terminal window

---

**Ready to explore 1,000 legal cases? Start now!** 🚀

```bash
./start.sh
```

Then open: **http://localhost:5000**

