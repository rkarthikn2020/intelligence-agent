"""
Database module for PostgreSQL + pgvector
Handles articles, uploaded documents, and vector embeddings
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import json

# Get DATABASE_URL from environment (Railway provides this automatically)
DATABASE_URL = os.getenv('DATABASE_URL')

def get_connection():
    """Get PostgreSQL connection"""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set!")
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    """Initialize PostgreSQL database (vectors stored as JSON)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Articles table with vector support (JSON format - no pgvector needed!)
        print("📊 Creating articles table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                source TEXT NOT NULL,
                summary TEXT,
                topics TEXT,
                content TEXT,
                full_content TEXT,
                published_date TIMESTAMP,
                scraped_date TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                word_count INTEGER DEFAULT 0,
                vector_indexed BOOLEAN DEFAULT FALSE,
                last_indexed_at TIMESTAMP,
                embedding TEXT
            )
        ''')
        
        # Index for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS articles_vector_indexed_idx 
            ON articles(vector_indexed) WHERE vector_indexed = TRUE
        ''')
        
        # Uploaded documents table
        print("📁 Creating uploaded_documents table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS uploaded_documents (
                id SERIAL PRIMARY KEY,
                filename TEXT NOT NULL,
                original_filename TEXT,
                file_type TEXT NOT NULL,
                file_path TEXT,
                file_size INTEGER,
                extracted_text TEXT,
                structured_data TEXT,
                word_count INTEGER DEFAULT 0,
                page_count INTEGER,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed BOOLEAN DEFAULT FALSE,
                vector_indexed BOOLEAN DEFAULT FALSE,
                last_indexed_at TIMESTAMP,
                uploaded_by TEXT,
                metadata TEXT,
                embedding TEXT
            )
        ''')
        
        # Index for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS documents_vector_indexed_idx 
            ON uploaded_documents(vector_indexed) WHERE vector_indexed = TRUE
        ''')
        
        # System configuration table
        print("⚙️  Creating system_config table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_config (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Daily summaries table
        print("📅 Creating daily_summaries table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_summaries (
                id SERIAL PRIMARY KEY,
                date DATE UNIQUE NOT NULL,
                summary TEXT NOT NULL,
                article_count INTEGER,
                topics TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        print("✅ Database initialized successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error initializing database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def save_article(article_data):
    """Save article to database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO articles 
            (title, url, source, summary, topics, content, full_content, 
             published_date, scraped_date, word_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO UPDATE SET
                summary = EXCLUDED.summary,
                topics = EXCLUDED.topics,
                content = EXCLUDED.content,
                full_content = EXCLUDED.full_content,
                word_count = EXCLUDED.word_count
            RETURNING id
        ''', (
            article_data.get('title', ''),
            article_data.get('url', ''),
            article_data.get('source', ''),
            article_data.get('summary', ''),
            json.dumps(article_data.get('topics', [])),
            article_data.get('content', ''),
            article_data.get('full_content', ''),
            article_data.get('published_date'),
            article_data.get('scraped_date', datetime.now()),
            article_data.get('word_count', 0)
        ))
        
        result = cursor.fetchone()
        conn.commit()
        return result['id'] if result else None
        
    except Exception as e:
        conn.rollback()
        print(f"Error saving article: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_recent_articles(days=7, limit=100):
    """Get recent articles from the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT * FROM articles 
            WHERE scraped_date >= CURRENT_TIMESTAMP - INTERVAL '%s days'
            ORDER BY scraped_date DESC 
            LIMIT %s
        ''', (days, limit))
        
        articles = cursor.fetchall()
        return articles
        
    finally:
        cursor.close()
        conn.close()

def save_daily_summary(date, summary, article_count, topics):
    """Save daily summary"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO daily_summaries (date, summary, article_count, topics)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (date) DO UPDATE SET
                summary = EXCLUDED.summary,
                article_count = EXCLUDED.article_count,
                topics = EXCLUDED.topics
        ''', (date, summary, article_count, json.dumps(topics)))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"Error saving daily summary: {e}")
    finally:
        cursor.close()
        conn.close()

def get_article_count():
    """Get total article count"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT COUNT(*) as count FROM articles')
        result = cursor.fetchone()
        return result['count'] if result else 0
        
    finally:
        cursor.close()
        conn.close()

def save_uploaded_document(doc_data):
    """Save uploaded document metadata"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO uploaded_documents 
            (filename, original_filename, file_type, file_path, file_size,
             extracted_text, word_count, page_count, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            doc_data.get('filename'),
            doc_data.get('original_filename'),
            doc_data.get('file_type'),
            doc_data.get('file_path'),
            doc_data.get('file_size', 0),
            doc_data.get('extracted_text', ''),
            doc_data.get('word_count', 0),
            doc_data.get('page_count', 0),
            json.dumps(doc_data.get('metadata', {}))
        ))
        
        result = cursor.fetchone()
        conn.commit()
        return result['id'] if result else None
        
    except Exception as e:
        conn.rollback()
        print(f"Error saving document: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_uploaded_documents(limit=50):
    """Get uploaded documents"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT * FROM uploaded_documents 
            ORDER BY upload_date DESC 
            LIMIT %s
        ''', (limit,))
        
        documents = cursor.fetchall()
        return documents
        
    finally:
        cursor.close()
        conn.close()

def update_vector_indexed(table, doc_id, indexed=True):
    """Mark document as vector indexed"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(f'''
            UPDATE {table}
            SET vector_indexed = %s, last_indexed_at = CURRENT_TIMESTAMP
            WHERE id = %s
        ''', (indexed, doc_id))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating vector index status: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Testing PostgreSQL connection...")
    try:
        init_db()
        print("✅ Database test successful!")
    except Exception as e:
        print(f"❌ Database test failed: {e}")
