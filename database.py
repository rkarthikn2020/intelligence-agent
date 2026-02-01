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
    
    # Articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            summary TEXT,
            topics TEXT,
            content TEXT,
            published_date TEXT,
            scraped_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

def save_article(title, url, source, summary, topics, content="", published_date=None):
    """Save an article to the database"""
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    
    try:
        scraped_date = datetime.now().strftime("%Y-%m-%d")
        topics_json = json.dumps(topics) if isinstance(topics, list) else topics
        
        cursor.execute('''
            INSERT OR REPLACE INTO articles 
            (title, url, source, summary, topics, content, published_date, scraped_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, url, source, summary, topics_json, content, published_date, scraped_date))
        
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
        SELECT title, source, summary, content, scraped_date, url FROM articles 
        WHERE scraped_date >= ?
        ORDER BY scraped_date DESC
    ''', (cutoff_date,))
    
    articles = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return articles

if __name__ == "__main__":
    init_db()
