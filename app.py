"""
Flask web application for the Intelligence Agent Dashboard
"""
from flask import Flask, render_template, request, jsonify
import database
import analyzer
import config
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# Initialize database when app starts (important for Railway)
database.init_db()

# Populate database on first startup
import os
if not os.path.exists('intelligence.db') or os.path.getsize('intelligence.db') < 5000:
    print("🔄 Database empty - running initial data collection...")
    try:
        import daily_job
        daily_job.run_daily_job()
        print("✅ Initial data collection complete!")
    except Exception as e:
        print(f"⚠️  Initial data collection failed: {e}")

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/articles')
def get_articles():
    """API endpoint to get recent articles"""
    days = request.args.get('days', 7, type=int)
    articles = database.get_recent_articles(days=days)
    
    # Group by date
    articles_by_date = {}
    for article in articles:
        date = article['scraped_date']
        if date not in articles_by_date:
            articles_by_date[date] = []
        articles_by_date[date].append(article)
    
    return jsonify({
        'success': True,
        'articles': articles,
        'by_date': articles_by_date,
        'count': len(articles)
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chatbot"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'success': False, 'error': 'No message provided'})
    
    # Get recent articles for context
    articles = database.get_all_articles_text(days=30)
    
    # Get response from Claude
    response = analyzer.get_chatbot_response(user_message, articles)
    
    return jsonify({
        'success': True,
        'response': response
    })

@app.route('/api/search')
def search():
    """API endpoint for searching articles"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'success': False, 'error': 'No query provided'})
    
    articles = database.search_articles(query)
    
    return jsonify({
        'success': True,
        'articles': articles,
        'count': len(articles),
        'query': query
    })

@app.route('/api/stats')
def stats():
    """API endpoint for dashboard statistics"""
    today_articles = database.get_today_articles()
    week_articles = database.get_recent_articles(days=7)
    
    # Count by source
    sources = {}
    for article in week_articles:
        source = article['source']
        sources[source] = sources.get(source, 0) + 1
    
    # Count by topic
    topics = {}
    for article in week_articles:
        article_topics = article.get('topics', [])
        if isinstance(article_topics, list):
            for topic in article_topics:
                topics[topic] = topics.get(topic, 0) + 1
    
    return jsonify({
        'success': True,
        'today_count': len(today_articles),
        'week_count': len(week_articles),
        'sources': sources,
        'topics': topics
    })

if __name__ == '__main__':
    # Run the Flask app
    print(f"🌐 Starting Dashboard on http://0.0.0.0:{config.PORT}")
    print(f"📊 Dashboard URL: http://localhost:{config.PORT}")
    app.run(host='0.0.0.0', port=config.PORT, debug=config.DEBUG)
