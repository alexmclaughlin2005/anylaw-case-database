#!/usr/bin/env python3
"""
Citation-Based Case Lookup Demo
Demonstrates how to find and cross-reference cases by their citations
"""

import json
from pathlib import Path

# Load the database
with open('Anylaw sample documents-b/index.json', 'r') as f:
    data = json.load(f)

print("=" * 70)
print("CITATION-BASED CASE LOOKUP DEMO")
print("=" * 70)
print()

# Step 1: Build Citation Index
print("STEP 1: Building Citation Index")
print("-" * 70)

citation_index = {}
for doc in data['documents']:
    citations = doc.get('cited_as', [])
    for citation in citations:
        citation_index[citation] = doc

print(f"✓ Created index with {len(citation_index)} citations")
print(f"✓ Covering {len(data['documents'])} cases")
print()

# Step 2: Look up a case by citation
print("STEP 2: Looking Up Cases by Citation")
print("-" * 70)

example_citations = [
    "251 F. Supp.2d 176",
    "524 A.2d 188", 
    "367 U.S. 1",
    "986 F.2d 728"
]

for cite in example_citations:
    if cite in citation_index:
        case = citation_index[cite]
        print(f"\nCitation: {cite}")
        print(f"  → Title: {case['title']}")
        print(f"  → Jurisdiction: {case['jurisdiction']}")
        print(f"  → Date: {case['date'][:10]}")
        print(f"  → Case ID: {case['id']}")
        print(f"  → File: {case['filename']}")
    else:
        print(f"\n✗ Citation not found: {cite}")

# Step 3: Find all cases from a specific reporter
print("\n" + "=" * 70)
print("STEP 3: Finding All Cases from Specific Reporters")
print("-" * 70)

def find_by_reporter(reporter_abbrev):
    """Find all cases from a specific reporter"""
    matches = []
    for citation, case in citation_index.items():
        if reporter_abbrev in citation:
            matches.append({
                'citation': citation,
                'title': case['title'],
                'jurisdiction': case['jurisdiction']
            })
    return matches

# Find all Supreme Court cases
supreme_court = find_by_reporter('U.S.')
print(f"\nU.S. Supreme Court Cases: {len(supreme_court)} found")
for i, case in enumerate(supreme_court[:5], 1):
    print(f"  {i}. {case['citation']} - {case['title']}")
if len(supreme_court) > 5:
    print(f"  ... and {len(supreme_court) - 5} more")

# Find all Federal Reporter cases
circuit_cases = find_by_reporter('F.2d')
print(f"\nFederal Circuit Court Cases (F.2d): {len(circuit_cases)} found")
for i, case in enumerate(circuit_cases[:5], 1):
    print(f"  {i}. {case['citation']} - {case['title']}")
if len(circuit_cases) > 5:
    print(f"  ... and {len(circuit_cases) - 5} more")

# Step 4: Reverse lookup - find all citations for a case
print("\n" + "=" * 70)
print("STEP 4: Finding All Citations for a Specific Case")
print("-" * 70)

# Pick a case with multiple citations
for doc in data['documents']:
    if len(doc.get('cited_as', [])) >= 3:
        print(f"\nCase: {doc['title']}")
        print(f"This case can be cited as:")
        for i, cite in enumerate(doc['cited_as'], 1):
            print(f"  {i}. {cite}")
        print(f"\nAll {len(doc['cited_as'])} citations point to the same case!")
        break

# Step 5: Demonstrate citation-based navigation
print("\n" + "=" * 70)
print("STEP 5: Citation-Based Navigation Example")
print("-" * 70)

print("\nScenario: I'm reading a case and see it cites '367 U.S. 1'")
print("Can I find that case in our database?")

target_citation = "367 U.S. 1"
if target_citation in citation_index:
    found_case = citation_index[target_citation]
    print(f"\n✓ YES! Found the case:")
    print(f"  Citation: {target_citation}")
    print(f"  Title: {found_case['title']}")
    print(f"  Jurisdiction: {found_case['jurisdiction']}")
    print(f"  File: {found_case['filename']}")
    print(f"\n  You can now load and read this case!")
else:
    print(f"\n✗ Sorry, '{target_citation}' is not in our database")

# Step 6: Summary statistics
print("\n" + "=" * 70)
print("CITATION INDEX STATISTICS")
print("=" * 70)

# Count cases by reporter type
reporter_counts = {}
for citation in citation_index.keys():
    # Extract reporter abbreviation (simplified)
    parts = citation.split()
    if len(parts) >= 2:
        reporter = parts[1]
        reporter_counts[reporter] = reporter_counts.get(reporter, 0) + 1

print(f"\nCitations by Reporter Type (top 10):")
top_reporters = sorted(reporter_counts.items(), key=lambda x: x[1], reverse=True)[:10]
for reporter, count in top_reporters:
    print(f"  {reporter:20} {count:4} citations")

print(f"\nTotal unique citations: {len(citation_index)}")
print(f"Total unique reporters: {len(reporter_counts)}")

# Cases with most parallel citations
print("\n" + "=" * 70)
print("CASES WITH MOST PARALLEL CITATIONS")
print("=" * 70)

cases_by_citation_count = sorted(
    data['documents'], 
    key=lambda x: len(x.get('cited_as', [])), 
    reverse=True
)

print("\nTop 5 cases with most parallel citations:")
for i, doc in enumerate(cases_by_citation_count[:5], 1):
    num_cites = len(doc.get('cited_as', []))
    print(f"\n{i}. {doc['title']}")
    print(f"   {num_cites} parallel citations:")
    for cite in doc['cited_as']:
        print(f"     • {cite}")

print("\n" + "=" * 70)
print("DEMO COMPLETE")
print("=" * 70)
print("\nKey Takeaways:")
print("1. ✓ You CAN look up cases by citation")
print("2. ✓ Build a citation_index dictionary for fast lookups")
print("3. ✓ Use citation strings as keys to find case data")
print("4. ✓ Multiple citations can point to the same case")
print("5. ✓ This enables cross-referencing between cases")
print()

