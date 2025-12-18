# Citation Cross-Reference Guide

## Yes, You CAN Reference Cases by Citation! ✓

Your database contains **1,925 unique citations** across **1,000 cases**. You can absolutely use citations to look up and cross-reference cases.

## Quick Answer

```python
# Build citation index
citation_index = {}
for doc in documents:
    for citation in doc.get('cited_as', []):
        citation_index[citation] = doc

# Look up a case
citation = "367 U.S. 1"
case = citation_index[citation]
# Returns: COMMUNIST PARTY UNITED STATES v. SUBVERSIVE ACTIVITIES CONTROL BOARD
```

## Understanding the Data

### What Citations Are In Your Data

The `cited_as` / `citedas` field tells you **how to cite THIS case**:

```json
{
  "title": "State v. Carr",
  "cited_as": [
    "300 Kan. 1",           // Kansas official reporter
    "331 P.3d 544",         // Pacific regional reporter
    "2014 WL 3681049",      // Westlaw
    "2014 Kan. LEXIS 432"   // LexisNexis
  ]
}
```

All 4 citations refer to the SAME case - just published in different reporters.

### What's NOT Explicitly in Your Data

The data **does NOT** have a separate field for:
- Cases that THIS case cites (outbound citations)
- Direct links between related cases

However, you CAN:
1. Build a citation index for lookups
2. Extract citations from case body text (advanced)
3. Create cross-reference networks

## How to Use Citations for Cross-Reference

### Method 1: Citation Lookup Index (Simple & Fast)

**Build the index once:**

```python
import json

# Load data
with open('Anylaw sample documents-b/index.json', 'r') as f:
    data = json.load(f)

# Build citation -> case mapping
citation_index = {}
for doc in data['documents']:
    for citation in doc.get('cited_as', []):
        citation_index[citation] = doc

print(f"Index built: {len(citation_index)} citations")
# Output: Index built: 1925 citations
```

**Use it for lookups:**

```python
# Find a case by citation
citation = "251 F. Supp.2d 176"
if citation in citation_index:
    case = citation_index[citation]
    print(f"Found: {case['title']}")
    print(f"ID: {case['id']}")
    print(f"File: {case['filename']}")
```

### Method 2: Using the Enhanced Flask App

I've added citation lookup to your app! New API endpoints:

**Find case by citation:**
```bash
GET /api/citation/251%20F.%20Supp.2d%20176
```

Response:
```json
{
  "id": "H42GQWYBTlTomsSBT--K",
  "title": "MCCONNELL v. FEDERAL ELECTION COMMISSION",
  "filename": "doc_0001_H42GQWYBTlTomsSBT--K.json",
  "jurisdiction": "District of Columbia",
  "date": "2003-05-01T00:00:00.000Z"
}
```

**Get all citations:**
```bash
GET /api/citations?limit=100
```

Response:
```json
{
  "citations": ["251 F. Supp.2d 176", "524 A.2d 188", ...],
  "total": 1925
}
```

### Method 3: Advanced - Extract Citations from Body Text

For finding cases that THIS case cites, you'd need to:

1. Load the full document
2. Parse the body text for citation patterns
3. Look up those citations in your index

```python
import re

def extract_citations_from_body(body_text):
    """Extract citation patterns from case body"""
    # Pattern: Volume Reporter Page (e.g., "367 U.S. 1")
    pattern = r'\b(\d+)\s+([A-Z][A-Za-z.]+\d*)\s+(\d+)\b'
    
    citations = []
    for match in re.finditer(pattern, body_text):
        volume, reporter, page = match.groups()
        citation = f"{volume} {reporter} {page}"
        citations.append(citation)
    
    return citations

# Load full document
with open('Anylaw sample documents-b/doc_0001.json', 'r') as f:
    doc = json.load(f)

# Extract citations this case references
body = doc['document']['body']
referenced_cases = extract_citations_from_body(body)

# Look them up in your database
for cite in referenced_cases:
    if cite in citation_index:
        print(f"Case cites: {citation_index[cite]['title']}")
```

**Note**: This is advanced and requires careful regex tuning to avoid false positives.

## Real Examples from Your Database

### Example 1: Look Up by Citation

```python
# Someone gives you a citation
citation = "367 U.S. 1"

# Find the case
case = citation_index[citation]

print(case['title'])
# Output: COMMUNIST PARTY UNITED STATES v. SUBVERSIVE ACTIVITIES CONTROL BOARD

print(case['jurisdiction'])
# Output: Supreme Court

print(case['filename'])
# Output: doc_0020_p9BJYmYBTlTomsSBE1h-.json
```

### Example 2: Find All Supreme Court Cases

```python
supreme_court_cases = []

for citation, case in citation_index.items():
    if 'U.S.' in citation and case['jurisdiction'] == 'Supreme Court':
        supreme_court_cases.append(case)

print(f"Found {len(supreme_court_cases)} Supreme Court cases")
# Output: Found 139 Supreme Court cases
```

### Example 3: Handle Parallel Citations

```python
# A case with multiple citations
case = citation_index["300 Kan. 1"]

print(f"Case: {case['title']}")
# Output: State v. Carr

print(f"All citations for this case:")
for cite in case['cited_as']:
    print(f"  - {cite}")

# Output:
#   - 300 Kan. 1
#   - 331 P.3d 544
#   - 2014 WL 3681049
#   - 2014 Kan. LEXIS 432

# All 4 lookups return the SAME case:
assert citation_index["300 Kan. 1"] == citation_index["331 P.3d 544"]
# True!
```

## Statistics from Your Database

Based on your 1,000 case sample:

| Metric | Value |
|--------|-------|
| Total cases | 1,000 |
| Total unique citations | 1,925 |
| Average citations per case | 1.96 |
| Cases with multiple citations | 58.5% |
| Most citations for one case | 5 |
| Unique reporter types | 78 |

**Top Reporters in Your Database:**
1. Cal. (California) - 237 citations
2. P.2d (Pacific 2d) - 228 citations
3. F.2d (Federal 2d) - 178 citations
4. F.3d (Federal 3d) - 147 citations
5. A.2d (Atlantic 2d) - 124 citations

## Code Examples

### Python Function: Citation Lookup

```python
def lookup_case_by_citation(citation, citation_index):
    """
    Find a case by its citation string.
    
    Args:
        citation: Citation string (e.g., "367 U.S. 1")
        citation_index: Pre-built citation index
    
    Returns:
        Case dict if found, None otherwise
    """
    return citation_index.get(citation)

# Usage
case = lookup_case_by_citation("367 U.S. 1", citation_index)
if case:
    print(f"Found: {case['title']}")
else:
    print("Citation not in database")
```

### Python Function: Find By Reporter

```python
def find_cases_by_reporter(reporter, citation_index):
    """
    Find all cases from a specific reporter.
    
    Args:
        reporter: Reporter abbreviation (e.g., "F.2d", "U.S.")
    
    Returns:
        List of matching cases
    """
    matches = []
    for citation, case in citation_index.items():
        if reporter in citation:
            # Avoid false matches
            if f" {reporter} " in f" {citation} ":
                matches.append({
                    'citation': citation,
                    'case': case
                })
    return matches

# Usage
supreme_court = find_cases_by_reporter("U.S.", citation_index)
print(f"Found {len(supreme_court)} Supreme Court cases")
```

### JavaScript Function: API Call

```javascript
// Look up case by citation
async function findCaseByCitation(citation) {
    const encoded = encodeURIComponent(citation);
    const response = await fetch(`/api/citation/${encoded}`);
    
    if (response.ok) {
        const case_info = await response.json();
        console.log(`Found: ${case_info.title}`);
        return case_info;
    } else {
        console.log('Citation not found');
        return null;
    }
}

// Usage
const caseInfo = await findCaseByCitation("367 U.S. 1");
```

## Use Cases

### 1. Citation Verification

"Does our database contain this case?"

```python
def verify_citation(citation):
    if citation in citation_index:
        case = citation_index[citation]
        return f"✓ Yes: {case['title']}"
    else:
        return "✗ Not in database"

print(verify_citation("367 U.S. 1"))
# Output: ✓ Yes: COMMUNIST PARTY UNITED STATES v. ...
```

### 2. Building a Related Cases Network

```python
def find_related_cases(case_id):
    """
    Find cases that might be related based on citations
    (same case, different citation)
    """
    # Find the case
    original = None
    for doc in documents:
        if doc['id'] == case_id:
            original = doc
            break
    
    if not original:
        return []
    
    # All citations for this case point to the same case
    related = []
    for citation in original.get('cited_as', []):
        if citation in citation_index:
            related.append({
                'citation': citation,
                'case': citation_index[citation]
            })
    
    return related
```

### 3. Citation Format Standardization

```python
def normalize_citation(citation):
    """
    Normalize citation format for better matching
    """
    # Remove extra spaces
    citation = ' '.join(citation.split())
    
    # Standardize periods
    citation = citation.replace(' . ', '.')
    
    return citation

# Usage
variants = [
    "367 U.S. 1",
    "367  U.S.  1",
    "367 U. S. 1"
]

for variant in variants:
    normalized = normalize_citation(variant)
    # Now look up the normalized version
```

## Limitations & Considerations

### What Works Great ✓

1. **Direct lookups**: Finding a case by its exact citation
2. **Parallel citations**: Multiple citations to same case
3. **Reporter filtering**: Finding all cases from a specific reporter
4. **Fast performance**: Index lookups are O(1)

### Limitations ⚠️

1. **Exact match required**: Citation must match exactly
   - "367 U.S. 1" works
   - "367 US 1" (no periods) won't match
   - Solution: Normalize citations before lookup

2. **No outbound citations**: Data doesn't explicitly list cases that this case cites
   - Solution: Parse body text (advanced, requires regex)

3. **Not all cases cite each other**: Your 1,000 cases may not have many internal references
   - The full 8.5M database would have more connections

4. **Incomplete coverage**: If Case A cites Case B, but Case B isn't in your sample, you can't follow the link

### Best Practices

1. **Build index once**: Create citation_index at startup, reuse it
2. **Normalize input**: Clean user-entered citations before lookup
3. **Handle missing**: Always check if citation exists before accessing
4. **Cache results**: Store frequently accessed cases in memory

## Testing Your Citation Lookups

Run the demo script:

```bash
cd "/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw"
python3 citation_lookup_demo.py
```

Or test via the API:

```bash
# Start the app
python3 app.py

# In another terminal, test the API
curl "http://localhost:5000/api/citation/367%20U.S.%201"
```

## Summary

**Yes, you CAN absolutely reference cases by citation!**

✓ Build a `citation_index` dictionary  
✓ Use citation strings as lookup keys  
✓ Handle parallel citations (multiple citations → same case)  
✓ Filter by reporter type  
✓ Enhanced Flask app includes citation APIs  

**Your database has:**
- 1,925 unique citations
- Covering 1,000 cases
- Average 1.96 citations per case
- 78 different reporter types

**Next steps:**
1. Run `citation_lookup_demo.py` to see examples
2. Use `/api/citation/<citation>` endpoint in your app
3. Build features that leverage citation cross-referencing

---

**For more information:**
- See `CITATIONS_GUIDE.md` for citation format details
- See `AI_Instructions.md` for API documentation
- See `citation_lookup_demo.py` for code examples

