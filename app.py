"""
AnyLaw Case Database Navigator
Main Flask application for browsing and analyzing the Lexsphere caselaw database
"""
import json
import os
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict
from flask import Flask, render_template, jsonify, request
from functools import lru_cache

app = Flask(__name__)

# Configuration
DATA_DIR = Path(__file__).parent / "Anylaw sample documents-b"
INDEX_FILE = DATA_DIR / "index.json"

# Word cloud exclusion list (from memory)
EXCLUDED_WORDS = {'details', 'page', 'https', 'filevineapp', 'docviewer', 
                   'view', 'source', 'embedding', 'the', 'and', 'or', 'of',
                   'to', 'in', 'a', 'is', 'that', 'for', 'with', 'as', 'on',
                   'be', 'at', 'by', 'this', 'from', 'it', 'an', 'are', 'was',
                   'not', 'but', 'have', 'had', 'has', 'will', 'would', 'been'}


class CaseLawDatabase:
    """Manages the caselaw database with caching and indexing"""
    
    def __init__(self, data_dir, index_file):
        self.data_dir = Path(data_dir)
        self.index_file = Path(index_file)
        self._index = None
        self._stats = None
        self._citation_index = None
        
    @property
    def index(self):
        """Lazy load the index file"""
        if self._index is None:
            with open(self.index_file, 'r') as f:
                data = json.load(f)
                self._index = data.get('documents', [])
        return self._index
    
    def get_stats(self):
        """Calculate database statistics"""
        if self._stats is not None:
            return self._stats
            
        docs = self.index
        jurisdictions = Counter()
        years = Counter()
        courts = defaultdict(int)
        total_citations = 0
        body_lengths = []
        
        for doc in docs:
            # Jurisdiction
            if 'jurisdiction' in doc:
                jurisdictions[doc['jurisdiction']] += 1
            
            # Year
            if 'date' in doc:
                try:
                    date = datetime.fromisoformat(doc['date'].replace('Z', '+00:00'))
                    years[date.year] += 1
                except:
                    pass
            
            # Citations
            if 'cited_as' in doc and doc['cited_as']:
                total_citations += len(doc['cited_as'])
            
            # Body length
            if 'body_length' in doc:
                body_lengths.append(doc['body_length'])
        
        self._stats = {
            'total_cases': len(docs),
            'jurisdictions': dict(jurisdictions.most_common(20)),
            'years': dict(sorted(years.items())),
            'avg_body_length': sum(body_lengths) / len(body_lengths) if body_lengths else 0,
            'total_citations': total_citations,
            'date_range': {
                'earliest': min(years.keys()) if years else None,
                'latest': max(years.keys()) if years else None
            }
        }
        
        return self._stats
    
    def search(self, query='', jurisdiction=None, year=None, limit=50, offset=0):
        """Search cases with filters"""
        results = self.index
        
        # Filter by jurisdiction
        if jurisdiction:
            results = [d for d in results if d.get('jurisdiction', '').lower() == jurisdiction.lower()]
        
        # Filter by year
        if year:
            results = [d for d in results if year in d.get('date', '')]
        
        # Search query (simple text search in title and jurisdiction)
        if query:
            query_lower = query.lower()
            results = [d for d in results if 
                      query_lower in d.get('title', '').lower() or
                      query_lower in d.get('jurisdiction', '').lower() or
                      query_lower in d.get('full_title', '').lower()]
        
        total = len(results)
        results = results[offset:offset + limit]
        
        return {
            'results': results,
            'total': total,
            'limit': limit,
            'offset': offset
        }
    
    def get_document(self, doc_id):
        """Get full document by ID"""
        # Find the document in index
        doc_info = next((d for d in self.index if d.get('id') == doc_id), None)
        if not doc_info:
            return None
        
        # Load the full document from file
        filename = doc_info.get('filename')
        if not filename:
            return None
        
        filepath = self.data_dir / filename
        if not filepath.exists():
            return None
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def get_jurisdictions(self):
        """Get list of all jurisdictions"""
        jurisdictions = set()
        for doc in self.index:
            if 'jurisdiction' in doc:
                jurisdictions.add(doc['jurisdiction'])
        return sorted(list(jurisdictions))
    
    @property
    def citation_index(self):
        """Build and cache citation lookup index"""
        if self._citation_index is None:
            self._citation_index = {}
            for doc in self.index:
                doc_id = doc['id']
                citations = doc.get('cited_as', [])
                
                for citation in citations:
                    # Map each citation to its case
                    self._citation_index[citation] = {
                        'id': doc_id,
                        'title': doc.get('title'),
                        'filename': doc.get('filename'),
                        'jurisdiction': doc.get('jurisdiction'),
                        'date': doc.get('date')
                    }
        return self._citation_index
    
    def find_by_citation(self, citation):
        """Find a case by its citation string"""
        return self.citation_index.get(citation)
    
    def get_all_citations(self):
        """Get list of all citations in the database"""
        return sorted(list(self.citation_index.keys()))


# Initialize database
db = CaseLawDatabase(DATA_DIR, INDEX_FILE)


# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/stats')
def api_stats():
    """Get database statistics"""
    return jsonify(db.get_stats())


@app.route('/api/jurisdictions')
def api_jurisdictions():
    """Get list of jurisdictions"""
    return jsonify(db.get_jurisdictions())


@app.route('/api/search')
def api_search():
    """Search endpoint"""
    query = request.args.get('q', '')
    jurisdiction = request.args.get('jurisdiction', None)
    year = request.args.get('year', None)
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    results = db.search(query, jurisdiction, year, limit, offset)
    return jsonify(results)


@app.route('/api/document/<doc_id>')
def api_document(doc_id):
    """Get full document with extracted citations"""
    import re
    from difflib import SequenceMatcher
    
    doc = db.get_document(doc_id)
    if not doc:
        return jsonify({'error': 'Document not found'}), 404
    
    # Extract citations from body text
    body = doc['document'].get('body', '')
    if body:
        # METHOD 1: Numeric citations (Volume Reporter Page)
        numeric_pattern = r'\b(\d+)\s+([A-Z][A-Za-z.]+(?:\s+[A-Za-z.]+)?)\s+(\d+)\b'
        numeric_matches = re.findall(numeric_pattern, body)
        
        # Build unique numeric citation list
        numeric_citations = set()
        for volume, reporter, page in numeric_matches:
            citation = f"{volume} {reporter} {page}"
            # Filter out obvious non-citations
            if not any(x in reporter.lower() for x in ['cong', 'stat', 'rec']):
                numeric_citations.add(citation)
        
        # Check which numeric citations are in our database
        outbound_numeric = []
        for cite in list(numeric_citations)[:100]:  # Limit to first 100
            case_info = db.find_by_citation(cite)
            if case_info and case_info['id'] != doc_id:
                outbound_numeric.append({
                    'citation': cite,
                    'id': case_info['id'],
                    'title': case_info['title'],
                    'type': 'numeric'
                })
        
        # METHOD 2: Case name matching
        # Pattern for case names: "Word(s) v. Word(s)" or "Word(s) v Word(s)"
        case_name_pattern = r'\b([A-Z][A-Za-z\'\s&.-]{2,40})\s+v\.?\s+([A-Z][A-Za-z\'\s&.-]{2,40})\b'
        case_name_matches = re.findall(case_name_pattern, body[:100000])  # First 100k chars for performance
        
        # Build title index for fuzzy matching
        title_to_case = {}
        for index_doc in db.index:
            title_to_case[index_doc['title'].lower()] = index_doc
        
        outbound_names = []
        seen_ids = set(item['id'] for item in outbound_numeric)  # Avoid duplicates
        
        for plaintiff, defendant in case_name_matches[:200]:  # Limit to first 200
            case_name = f"{plaintiff.strip()} v. {defendant.strip()}"
            
            # Skip if too long (probably not a case name)
            if len(case_name) > 80:
                continue
            
            # Try exact match first
            case_name_lower = case_name.lower()
            if case_name_lower in title_to_case:
                matched = title_to_case[case_name_lower]
                if matched['id'] != doc_id and matched['id'] not in seen_ids:
                    outbound_names.append({
                        'citation': case_name,
                        'id': matched['id'],
                        'title': matched['title'],
                        'type': 'case_name'
                    })
                    seen_ids.add(matched['id'])
                    if len(outbound_names) >= 20:  # Limit case name matches
                        break
                continue
            
            # Try fuzzy matching (find best match)
            best_match = None
            best_score = 0.0
            
            for db_title, db_case in title_to_case.items():
                # Quick check if both plaintiff and defendant appear
                if plaintiff.strip().lower() in db_title and defendant.strip().lower() in db_title:
                    score = SequenceMatcher(None, case_name_lower, db_title).ratio()
                    if score > best_score and score > 0.8:  # 80% similarity threshold
                        best_score = score
                        best_match = db_case
            
            if best_match and best_match['id'] != doc_id and best_match['id'] not in seen_ids:
                outbound_names.append({
                    'citation': case_name,
                    'id': best_match['id'],
                    'title': best_match['title'],
                    'type': 'case_name',
                    'match_score': round(best_score * 100)
                })
                seen_ids.add(best_match['id'])
                if len(outbound_names) >= 20:  # Limit case name matches
                    break
        
        # Combine results
        doc['extracted_citations'] = {
            'total_numeric_found': len(numeric_citations),
            'total_names_found': len(set(f"{p} v. {d}" for p, d in case_name_matches)),
            'numeric_matches': outbound_numeric,
            'name_matches': outbound_names,
            'total_in_database': len(outbound_numeric) + len(outbound_names)
        }
    
    return jsonify(doc)


@app.route('/case/<doc_id>')
def case_detail(doc_id):
    """Case detail page"""
    return render_template('case.html', doc_id=doc_id)


@app.route('/search')
def search_page():
    """Search page"""
    return render_template('search.html')


@app.route('/api/citation/<path:citation>')
def api_find_by_citation(citation):
    """Find case by citation string"""
    result = db.find_by_citation(citation)
    if result:
        return jsonify(result)
    return jsonify({'error': 'Citation not found'}), 404


@app.route('/api/citations')
def api_all_citations():
    """Get all citations in database"""
    limit = int(request.args.get('limit', 100))
    citations = db.get_all_citations()[:limit]
    return jsonify({
        'citations': citations,
        'total': len(db.citation_index)
    })


if __name__ == '__main__':
    print("Starting AnyLaw Case Database Navigator...")
    print(f"Data directory: {DATA_DIR}")
    print(f"Loading index from: {INDEX_FILE}")
    
    # Warm up the cache
    stats = db.get_stats()
    print(f"Loaded {stats['total_cases']} cases")
    
    app.run(debug=True, port=5000)

