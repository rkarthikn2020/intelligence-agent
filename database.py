"""
Database module for storing articles and summaries
"""
import sqlite3
from datetime import datetime, timedelta
import json
import config

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    
    # Articles table (enhanced with full content and vector status)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            summary TEXT,
            topics TEXT,
            content TEXT,
            full_content TEXT,
            published_date TEXT,
            scraped_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            word_count INTEGER DEFAULT 0,
            vector_indexed BOOLEAN DEFAULT 0,
            last_indexed_at TIMESTAMP
        )
    ''')
    
    # Uploaded documents table (NEW)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploaded_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            extracted_text TEXT,
            structured_data TEXT,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed BOOLEAN DEFAULT 0,
            vector_indexed BOOLEAN DEFAULT 0,
            metadata TEXT,
            file_size INTEGER
        )
    ''')
    
    # System configuration table (NEW)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indices for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_articles_date ON articles(scraped_date DESC)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_articles_vector ON articles(vector_indexed)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_uploads_date ON uploaded_documents(upload_date DESC)')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

def save_article(title, url, source, summary, topics, content="", full_content="", published_date=None):
    """Save an article to the database"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    
    try:
        scraped_date = datetime.now().strftime("%Y-%m-%d")
        topics_json = json.dumps(topics) if isinstance(topics, list) else topics
        
        # Calculate word count
        text_for_count = full_content if full_content else content
        word_count = len(text_for_count.split()) if text_for_count else 0
        
        cursor.execute('''
            INSERT OR REPLACE INTO articles 
            (title, url, source, summary, topics, content, full_content, published_date, scraped_date, word_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, url, source, summary, topics_json, content, full_content, published_date, scraped_date, word_count))
        
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"⚠️  Article already exists: {url}")
        return None
    finally:
        conn.close()

def get_recent_articles(days=7):
    """Get articles from the last N days"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    cursor.execute('''
        SELECT * FROM articles 
        WHERE scraped_date >= ?
        ORDER BY scraped_date DESC, created_at DESC
    ''', (cutoff_date,))
    
    articles = [dict(row) for row in cursor.fetchall()]
    
    # Parse topics JSON
    for article in articles:
        if article['topics']:
            try:
                article['topics'] = json.loads(article['topics'])
            except:
                article['topics'] = []
    
    conn.close()
    return articles

def get_today_articles():
    """Get articles scraped today"""
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(config.DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM articles 
        WHERE scraped_date = ?
        ORDER BY created_at DESC
    ''', (today,))
    
    articles = [dict(row) for row in cursor.fetchall()]
    
    # Parse topics JSON
    for article in articles:
        if article['topics']:
            try:
                article['topics'] = json.loads(article['topics'])
            except:
                article['topics'] = []
    
    conn.close()
    return articles

def search_articles(query, days=30):
    """Search articles by keyword"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    search_term = f"%{query}%"
    
    cursor.execute('''
        SELECT * FROM articles 
        WHERE scraped_date >= ?
        AND (title LIKE ? OR summary LIKE ? OR content LIKE ?)
        ORDER BY scraped_date DESC, created_at DESC
        LIMIT 50
    ''', (cutoff_date, search_term, search_term, search_term))
    
    articles = [dict(row) for row in cursor.fetchall()]
    
    # Parse topics JSON
    for article in articles:
        if article['topics']:
            try:
                article['topics'] = json.loads(article['topics'])
            except:
                article['topics'] = []
    
    conn.close()
    return articles

def get_all_articles_text(days=30):
    """Get all article content for chatbot context"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    cursor.execute('''
        SELECT title, source, summary, content, full_content, scraped_date, url FROM articles 
        WHERE scraped_date >= ?
        ORDER BY scraped_date DESC
    ''', (cutoff_date,))
    
    articles = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return articles

# ============================================================================
# NEW FUNCTIONS FOR ENHANCED FEATURES
# ============================================================================

def save_uploaded_document(filename, file_type, extracted_text, structured_data=None, metadata=None, file_size=0):
    """Save an uploaded document to the database"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    
    try:
        structured_json = json.dumps(structured_data) if structured_data else None
        metadata_json = json.dumps(metadata) if metadata else None
        
        cursor.execute('''
            INSERT INTO uploaded_documents 
            (filename, file_type, extracted_text, structured_data, metadata, file_size, processed)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ''', (filename, file_type, extracted_text, structured_json, metadata_json, file_size))
        
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"❌ Error saving uploaded document: {e}")
        return None
    finally:
        conn.close()

def get_uploaded_documents(days=30):
    """Get recently uploaded documents"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        SELECT * FROM uploaded_documents 
        WHERE upload_date >= ?
        ORDER BY upload_date DESC
    ''', (cutoff_date,))
    
    docs = [dict(row) for row in cursor.fetchall()]
    
    # Parse JSON fields
    for doc in docs:
        if doc['structured_data']:
            try:
                doc['structured_data'] = json.loads(doc['structured_data'])
            except:
                doc['structured_data'] = None
        if doc['metadata']:
            try:
                doc['metadata'] = json.loads(doc['metadata'])
            except:
                doc['metadata'] = {}
    
    conn.close()
    return docs

def mark_document_indexed(doc_id, doc_type='article'):
    """Mark a document as vector indexed"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    
    table = 'articles' if doc_type == 'article' else 'uploaded_documents'
    timestamp = datetime.now().isoformat()
    
    cursor.execute(f'''
        UPDATE {table}
        SET vector_indexed = 1, last_indexed_at = ?
        WHERE id = ?
    ''', (timestamp, doc_id))
    
    conn.commit()
    conn.close()

def get_unindexed_documents(doc_type='all'):
    """Get documents that haven't been vector indexed yet"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    
    documents = []
    
    if doc_type in ['all', 'article']:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title as filename, full_content as text, 'article' as type
            FROM articles 
            WHERE vector_indexed = 0 AND full_content IS NOT NULL AND full_content != ''
            ORDER BY created_at DESC
            LIMIT 100
        ''')
        documents.extend([dict(row) for row in cursor.fetchall()])
    
    if doc_type in ['all', 'upload']:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, filename, extracted_text as text, 'upload' as type
            FROM uploaded_documents 
            WHERE vector_indexed = 0 AND extracted_text IS NOT NULL AND extracted_text != ''
            ORDER BY upload_date DESC
            LIMIT 100
        ''')
        documents.extend([dict(row) for row in cursor.fetchall()])
    
    conn.close()
    return documents

def save_config(key, value):
    """Save system configuration"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    cursor.execute('''
        INSERT OR REPLACE INTO system_config (key, value, updated_at)
        VALUES (?, ?, ?)
    ''', (key, value, timestamp))
    
    conn.commit()
    conn.close()

def get_config(key, default=None):
    """Get system configuration"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT value FROM system_config WHERE key = ?', (key,))
    row = cursor.fetchone()
    
    conn.close()
    return row[0] if row else default

def get_all_config():
    """Get all system configuration"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM system_config ORDER BY key')
    configs = {row['key']: row['value'] for row in cursor.fetchall()}
    
    conn.close()
    return configs

def get_stats():
    """Get database statistics"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    
    stats = {}
    
    # Article counts
    cursor.execute('SELECT COUNT(*) FROM articles')
    stats['total_articles'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM articles WHERE vector_indexed = 1')
    stats['indexed_articles'] = cursor.fetchone()[0]
    
    # Upload counts
    cursor.execute('SELECT COUNT(*) FROM uploaded_documents')
    stats['total_uploads'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM uploaded_documents WHERE vector_indexed = 1')
    stats['indexed_uploads'] = cursor.fetchone()[0]
    
    # Sources
    cursor.execute('SELECT source, COUNT(*) as count FROM articles GROUP BY source')
    stats['by_source'] = dict(cursor.fetchall())
    
    conn.close()
    return stats

if __name__ == "__main__":
    init_db()
