# Using Citation Lookup in the UI

## ✅ Now Available in the Web Interface!

The citation lookup feature is now integrated into the search page with a beautiful tabbed interface.

## 🚀 How to Use

### Step 1: Navigate to Search
1. Start the app: `python3 app.py`
2. Open browser to: `http://localhost:5000`
3. Click **"Search Cases"** in the navigation

### Step 2: Switch to Citation Lookup Tab
- You'll see two tabs at the top:
  - **Text Search** (default)
  - **Citation Lookup** ← Click this!

### Step 3: Enter a Citation
Type a legal citation in the search box, for example:
- `367 U.S. 1`
- `251 F. Supp.2d 176`
- `524 A.2d 188`
- `300 Kan. 1`

### Step 4: Find the Case
- Click **"Find Case"** button
- OR press **Enter**

### Step 5: View Results
If found, you'll see:
- ✅ A highlighted result with the citation badge
- Case title (clickable)
- Jurisdiction
- Date
- Case ID
- **"View Full Case"** button

If not found:
- ❌ Helpful error message with tips
- Suggestions for alternative searches

## 📖 Example Citations to Try

From your database (guaranteed to work):

### Supreme Court Cases
```
367 U.S. 1
400 U.S. 112
438 U.S. 265
369 U.S. 186
```

### Federal Circuit Courts
```
986 F.2d 728
708 F.2d 1081
892 F.2d 851
```

### Federal District Courts
```
251 F. Supp.2d 176
```

### State Cases
```
300 Kan. 1
524 A.2d 188
106 N.J. 123
272 Conn. 106
```

### Cases with Multiple Citations
Try both of these - they're the SAME case:
```
300 Kan. 1
331 P.3d 544
```

## 🎨 What You'll See

### Citation Found
```
┌─────────────────────────────────────────────────────┐
│ 📖 367 U.S. 1                                       │
│                                                      │
│ COMMUNIST PARTY UNITED STATES v.                    │
│ SUBVERSIVE ACTIVITIES CONTROL BOARD                 │
│                                                      │
│ 📍 Supreme Court   📅 Jun 5, 1961                   │
│ 🆔 p9BJYmYBTlTomsSBE1h-                             │
│                                                      │
│ [View Full Case]                                    │
└─────────────────────────────────────────────────────┘
```

### Citation Not Found
```
┌─────────────────────────────────────────────────────┐
│ 📖 Citation Not Found                               │
│                                                      │
│ The citation "123 F.4th 999" was not found          │
│                                                      │
│ Tips:                                               │
│ • Check the citation format                         │
│ • Ensure proper spacing and punctuation             │
│ • Try a different citation for the same case        │
│ • Use Text Search to find by title                  │
└─────────────────────────────────────────────────────┘
```

## 💡 Features

### Tabbed Interface
- **Text Search** - Search by keywords, titles, jurisdiction
- **Citation Lookup** - Direct lookup by citation
- Filters only show for text search
- Clean, intuitive switching between modes

### Smart Search
- Works with exact citation strings
- Case-sensitive matching
- Handles standard legal citation formats
- Press Enter to search

### Beautiful Results
- Citation displayed in a badge
- Color-coded result card
- Quick access to full case
- All key metadata visible

## 🔍 Use Cases

### 1. You Have a Citation Reference
Reading a legal brief that cites "367 U.S. 1"? Look it up instantly!

### 2. Verify a Case is in Database
Check if a specific case is available before digging deeper.

### 3. Quick Navigation
Fastest way to get to a specific case if you know the citation.

### 4. Cross-Reference
Following citations from one case to another.

## ⚙️ Technical Details

### API Endpoint Used
```
GET /api/citation/{citation}
```

### Response Format
```json
{
  "id": "case_id",
  "title": "Case Title",
  "filename": "doc_####_ID.json",
  "jurisdiction": "Court Name",
  "date": "2003-05-01T00:00:00.000Z"
}
```

### Frontend Implementation
- Tab-based navigation
- Real-time API calls
- Error handling with helpful messages
- Styled citation badges
- Responsive design

## 📊 Database Coverage

Your sample contains:
- **1,925 unique citations**
- **1,000 cases**
- **Average 1.96 citations per case**
- **58.5% have multiple citations**

Top citation types:
1. California cases: 237
2. Pacific Reporter: 228
3. Federal Reporter: 178
4. Atlantic Reporter: 124
5. U.S. Supreme Court: 139

## 🎯 Tips for Best Results

### Citation Format Matters
✅ **Good**: `367 U.S. 1`
❌ **Bad**: `367 US 1` (missing periods)
❌ **Bad**: `367  U.S.  1` (extra spaces)

### Exact Match Required
The citation must match exactly as stored in the database.

### Try Parallel Citations
If one citation doesn't work, try an alternative citation for the same case.

### Fall Back to Text Search
If citation lookup fails, switch to Text Search tab and search by case title.

## 🚦 Quick Start

**Try it now:**

1. Run: `python3 app.py`
2. Open: `http://localhost:5000/search`
3. Click: **Citation Lookup** tab
4. Type: `367 U.S. 1`
5. Press: **Enter**
6. See: Case details appear!

---

**Questions?**
- See `CITATION_CROSS_REFERENCE.md` for technical details
- See `CITATIONS_GUIDE.md` for citation format reference
- See `README.md` for general usage guide

