"""
AnyLaw Case Database Navigator - Backend API
Flask REST API for serving caselaw database
Designed for deployment on Railway
"""
import json
import os
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict
from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import lru_cache
import re

app = Flask(__name__)

# Configure CORS
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})

# Configuration
# When deployed to Railway with root directory 'backend', 
# the data is at ../Anylaw sample documents-b
if os.getenv('RAILWAY_ENVIRONMENT'):
    # Railway deployment - go up one level to find data
    DATA_DIR = Path(__file__).parent.parent / "Anylaw sample documents-b"
else:
    # Local development - use symlink or env var
    DATA_DIR = Path(os.getenv('DATA_DIR', Path(__file__).parent / "data"))

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


# Health check endpoint for Railway
@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'anylaw-backend',
        'version': '1.0.0'
    })

@app.route('/test')
def test():
    """Simple test endpoint that doesn't require data"""
    return jsonify({
        'message': 'Backend is running!',
        'python_version': '3.11',
        'flask': 'working',
        'data_dir': str(DATA_DIR),
        'data_exists': DATA_DIR.exists() if DATA_DIR else False,
        'index_exists': INDEX_FILE.exists() if INDEX_FILE else False
    })


# API Routes
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
    doc = db.get_document(doc_id)
    if not doc:
        return jsonify({'error': 'Document not found'}), 404
    
    # Extract citations from body text
    body = doc['document'].get('body', '')
    if body:
        # Pattern for legal citations: Volume Reporter Page
        pattern = r'\b(\d+)\s+([A-Z][A-Za-z.]+(?:\s+[A-Za-z.]+)?)\s+(\d+)\b'
        matches = re.findall(pattern, body)
        
        # Build unique citation list
        citations_found = set()
        for volume, reporter, page in matches:
            citation = f"{volume} {reporter} {page}"
            # Filter out obvious non-citations
            if not any(x in reporter.lower() for x in ['cong', 'stat', 'rec']):
                citations_found.add(citation)
        
        # Check which are in our database
        outbound_citations = []
        for cite in list(citations_found)[:100]:  # Limit to first 100
            case_info = db.find_by_citation(cite)
            if case_info and case_info['id'] != doc_id:
                outbound_citations.append({
                    'citation': cite,
                    'id': case_info['id'],
                    'title': case_info['title']
                })
        
        doc['extracted_citations'] = {
            'total_found': len(citations_found),
            'in_database': outbound_citations
        }
    
    return jsonify(doc)


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


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Starting AnyLaw Backend API...")
    print(f"Data directory: {DATA_DIR}")
    print(f"Loading index from: {INDEX_FILE}")
    
    # Warm up the cache
    stats = db.get_stats()
    print(f"Loaded {stats['total_cases']} cases")
    
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

