# Legal Citations Guide - Understanding Case Citation Data

## Quick Overview

**Citations** are standardized references that uniquely identify where a legal case is officially published. They work like URLs or ISBNs - they tell you exactly where to find the full text of a case.

## Field Names in Your Data

⚠️ **Important**: There's a naming inconsistency in the Lexsphere data:

- **In `index.json`**: Field is `"cited_as"` (with underscore)
- **In `doc_*.json` files**: Field is `"citedas"` (no underscore)

Both contain the same type of data - an array of citation strings.

## Data Structure

```json
{
  "cited_as": ["251 F. Supp.2d 176", "106 N.J. 123"],
  "citation_count": 0
}
```

## Understanding Citation Formats

### Basic Structure

Most citations follow this pattern:
```
[Volume Number] [Reporter Abbreviation] [Page Number]
```

Example: `251 F. Supp.2d 176`
- **251** = Volume number
- **F. Supp.2d** = Reporter name (Federal Supplement, 2nd Series)
- **176** = Starting page number

### Federal Court Citations

#### U.S. Supreme Court
```
367 U.S. 1
81 S. Ct. 1357
6 L. Ed. 2d 625
```

**Reporters:**
- `U.S.` = United States Reports (official)
- `S. Ct.` = Supreme Court Reporter (Thomson Reuters)
- `L. Ed.` = Lawyers' Edition (LexisNexis)

#### Federal Circuit Courts (Courts of Appeals)
```
986 F.2d 728
331 F.3d 544
```

**Reporters:**
- `F.` = Federal Reporter (1st Series, 1880-1924)
- `F.2d` = Federal Reporter, 2nd Series (1924-1993)
- `F.3d` = Federal Reporter, 3rd Series (1993-present)

#### Federal District Courts
```
251 F. Supp.2d 176
123 F. Supp.3d 456
```

**Reporters:**
- `F. Supp.` = Federal Supplement (1st Series)
- `F. Supp.2d` = Federal Supplement, 2nd Series
- `F. Supp.3d` = Federal Supplement, 3rd Series

### State Court Citations

#### Official State Reporters
```
300 Kan. 1        (Kansas)
106 N.J. 123      (New Jersey)
272 Conn. 106     (Connecticut)
```

Format: `[Volume] [State Abbreviation] [Page]`

#### Regional Reporters

West Publishing organizes state cases into regional reporters:

```
331 P.3d 544      (Pacific Reporter)
524 A.2d 188      (Atlantic Reporter)
864 A.2d 666      (Atlantic Reporter)
```

**Regional Reporter Coverage:**

| Reporter | States Covered |
|----------|----------------|
| `A.`, `A.2d`, `A.3d` | Atlantic: CT, DE, ME, MD, NH, NJ, PA, RI, VT, DC |
| `P.`, `P.2d`, `P.3d` | Pacific: AK, AZ, CA, CO, HI, ID, KS, MT, NV, NM, OK, OR, UT, WA, WY |
| `N.E.`, `N.E.2d`, `N.E.3d` | North Eastern: IL, IN, MA, NY, OH |
| `N.W.`, `N.W.2d` | North Western: IA, MI, MN, NE, ND, SD, WI |
| `S.E.`, `S.E.2d` | South Eastern: GA, NC, SC, VA, WV |
| `S.W.`, `S.W.2d`, `S.W.3d` | South Western: AR, KY, MO, TN, TX |
| `So.`, `So.2d`, `So.3d` | Southern: AL, FL, LA, MS |

### Online Database Citations

```
2014 WL 3681049         (Westlaw)
2014 Kan. LEXIS 432     (LexisNexis)
```

Format: `[Year] [Database] [Document Number]`

These are used for:
- Very recent cases not yet in print reporters
- Unpublished opinions
- Cases available only electronically

## Parallel Citations

**Why multiple citations for one case?**

A single case is often published in multiple places:

```json
"cited_as": [
  "300 Kan. 1",           // Official Kansas state reporter
  "331 P.3d 544",         // Pacific Regional reporter
  "2014 WL 3681049",      // Westlaw database
  "2014 Kan. LEXIS 432"   // LexisNexis database
]
```

This is called **parallel citation**. All four references point to the **same case**, just in different publications.

### Why This Matters

1. **Different libraries have different reporters** - lawyers can find it in whatever they have access to
2. **Some jurisdictions require specific reporters** - courts may mandate citing the official state reporter
3. **Historical reasons** - some reporters are older/more authoritative

## Real Examples from Your Database

### Example 1: Supreme Court Case
```json
{
  "title": "COMMUNIST PARTY UNITED STATES v. SUBVERSIVE ACTIVITIES CONTROL BOARD",
  "cited_as": [
    "81 S. Ct. 1357",     // Supreme Court Reporter
    "367 U.S. 1",         // U.S. Reports (official)
    "6 L. Ed. 2d 625"     // Lawyers' Edition
  ]
}
```

### Example 2: State Case with Full Parallel Citations
```json
{
  "title": "State v. Carr",
  "cited_as": [
    "300 Kan. 1",           // Kansas official reporter
    "331 P.3d 544",         // Pacific Reporter
    "2014 WL 3681049",      // Westlaw
    "2014 Kan. LEXIS 432"   // LexisNexis
  ]
}
```

### Example 3: Federal District Court (Single Citation)
```json
{
  "title": "MCCONNELL v. FEDERAL ELECTION COMMISSION",
  "cited_as": [
    "251 F. Supp.2d 176"    // Federal Supplement only
  ]
}
```

## Citation Count Field

```json
{
  "citation_count": 0
}
```

**What it means**: How many times **this case** has been **cited by other cases** in the database.

- **High count** (e.g., 100+) = Landmark case, frequently referenced
- **Medium count** (e.g., 10-50) = Important precedent
- **Low/Zero count** = Less influential or very recent

**Note**: The count is based on the database contents, not all cases ever published.

## Statistics from Your Database

Based on your 1,000 case sample:

- **Total cases**: 1,000
- **Total citations**: 1,959
- **Average citations per case**: 1.96
- **Cases with multiple citations**: 585 (58.5%)
- **Most citations for single case**: 5

This means:
- Most cases have 1-2 citations
- Over half have parallel citations
- The data is well-cited and comes from multiple sources

## How Citations Are Used in the App

### 1. Search Results
Shows the **first citation** as a badge:

```
State v. Carr
📍 Supreme Court of Kansas  📅 2014  📖 300 Kan. 1
```

### 2. Case Detail Page
Shows **all citations** in styled badges:

```
📖 Citations
┌─────────────────┬─────────────────┬─────────────────┬──────────────────┐
│ 300 Kan. 1      │ 331 P.3d 544    │ 2014 WL 3681049 │ 2014 Kan. LEXIS 432 │
└─────────────────┴─────────────────┴─────────────────┴──────────────────┘
```

## Working with Citations in Code

### Accessing Citations

```python
# From index.json
doc = index['documents'][0]
citations = doc.get('cited_as', [])  # Note: underscore

# From individual doc file
full_doc = load_document('doc_0001.json')
citations = full_doc['document'].get('citedas', [])  # Note: no underscore
```

### Displaying First Citation
```python
first_citation = citations[0] if citations else "No citation available"
```

### Counting Citations
```python
num_citations = len(citations)
has_parallel_cites = num_citations > 1
```

### Finding Cases by Reporter
```python
# Find all Supreme Court cases
supreme_court_cases = [
    doc for doc in documents 
    if any('U.S.' in cite for cite in doc.get('cited_as', []))
]

# Find all Kansas cases
kansas_cases = [
    doc for doc in documents
    if any('Kan.' in cite for cite in doc.get('cited_as', []))
]
```

## Common Citation Patterns

### By Court Level

| Court Type | Citation Pattern | Example |
|------------|------------------|---------|
| U.S. Supreme Court | `### U.S. ###` | `367 U.S. 1` |
| Federal Circuit | `### F.2d/F.3d ###` | `986 F.2d 728` |
| Federal District | `### F. Supp.2d ###` | `251 F. Supp.2d 176` |
| State Supreme | `### [State] ###` | `300 Kan. 1` |
| State (Regional) | `### A.2d/P.3d/etc ###` | `331 P.3d 544` |
| Online Only | `#### WL/LEXIS ####` | `2014 WL 3681049` |

## Tips for Analysis

### Finding Important Cases
```python
# Cases cited many times are often important
important_cases = [
    doc for doc in documents
    if doc.get('citation_count', 0) > 20
]
```

### Understanding Jurisdiction
The reporter abbreviation tells you the jurisdiction:
- `F.` = Federal
- `U.S.` = U.S. Supreme Court  
- `Kan.`, `N.J.`, `Conn.` = Specific states
- `P.`, `A.`, etc. = Regional (covers multiple states)

### Dating Cases
- `F.` (no number) = Very old (pre-1924)
- `F.2d` = 1924-1993
- `F.3d` = 1993-present
- Similar pattern for `A.`, `P.`, etc.

## FAQs

**Q: Why do some cases have only one citation?**
A: Newer cases, unpublished opinions, or cases only in online databases may have just one citation.

**Q: Which citation should I use?**
A: In legal writing, use the one required by court rules (usually the official reporter). For searching, any will work.

**Q: What if a case has no citations?**
A: Very rare in this database. Could indicate incomplete data or a very recent case.

**Q: Can I search by citation?**
A: Yes! The app's search will find cases if you enter a citation string.

**Q: What does "2d" or "3d" mean?**
A: Second Series, Third Series - reporters restart numbering periodically to keep volume numbers manageable.

## Resources for Learning More

- **The Bluebook**: Standard citation format guide
- **ALWD Guide**: Alternative citation manual
- **Cornell LII**: Free online legal citation guide

## Quick Reference Card

```
CITATION ANATOMY: 251 F. Supp.2d 176
                  ↑   ↑        ↑
                  │   │        └─ Page number
                  │   └─ Reporter (Federal Supplement, 2nd Series)
                  └─ Volume number

FINDING COURT LEVEL:
U.S. / S. Ct. / L. Ed. ────→ Supreme Court
F.2d / F.3d ───────────────→ Circuit Court (Appeals)
F. Supp.2d / F. Supp.3d ───→ District Court
State abbrev. + number ────→ State Court
WL / LEXIS ────────────────→ Online database

DATA FIELDS:
index.json      → "cited_as" (with underscore)
doc_*.json      → "citedas" (no underscore)
Both files      → "citation_count" (how many times cited)
```

---

**Last Updated**: December 17, 2025  
**Database**: Lexsphere Sample (1,000 cases)  
**For questions**: See AI_Instructions.md or README.md

