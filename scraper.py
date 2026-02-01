"""
Web scraper module for fetching articles from configured websites
"""
import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime
import config
import time

def scrape_rss_feed(feed_url, source_name):
    """Scrape articles from RSS feed"""
    articles = []
    try:
        print(f"🔍 Fetching RSS feed: {source_name}")
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries[:10]:  # Get last 10 articles
            article = {
                'title': entry.get('title', 'No Title'),
                'url': entry.get('link', ''),
                'source': source_name,
                'published': entry.get('published', entry.get('updated', '')),
                'summary': entry.get('summary', entry.get('description', ''))
            }
            
            # Get full content if available
            if 'content' in entry:
                article['content'] = entry.content[0].value
            elif 'description' in entry:
                article['content'] = entry.description
            else:
                article['content'] = article['summary']
            
            articles.append(article)
            
        print(f"✅ Found {len(articles)} articles from {source_name}")
    except Exception as e:
        print(f"❌ Error scraping {source_name}: {str(e)}")
    
    return articles

def scrape_koch_news():
    """Scrape Koch Inc news page"""
    articles = []
    try:
        print("🔍 Scraping Koch Inc newsroom")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get("https://www.kochinc.com/newsroom", headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for news articles (this may need adjustment based on actual site structure)
        # Koch's website structure may vary, this is a general approach
        news_items = soup.find_all(['article', 'div'], class_=['news-item', 'article', 'post'])[:10]
        
        for item in news_items:
            title_elem = item.find(['h1', 'h2', 'h3', 'h4', 'a'])
            if title_elem:
                title = title_elem.get_text(strip=True)
                link = item.find('a')
                url = link.get('href', '') if link else ''
                
                # Make sure URL is absolute
                if url and not url.startswith('http'):
                    url = 'https://www.kochinc.com' + url
                
                # Get summary/description
                summary_elem = item.find(['p', 'div'], class_=['summary', 'excerpt', 'description'])
                summary = summary_elem.get_text(strip=True) if summary_elem else ''
                
                if title and url:
                    articles.append({
                        'title': title,
                        'url': url,
                        'source': 'Koch Inc News',
                        'published': '',
                        'summary': summary,
                        'content': summary
                    })
        
        print(f"✅ Found {len(articles)} articles from Koch Inc")
    except Exception as e:
        print(f"❌ Error scraping Koch Inc: {str(e)}")
    
    return articles

def scrape_all_sources():
    """Scrape all configured websites"""
    all_articles = []
    
    for source_name, source_config in config.WEBSITES.items():
        try:
            if source_config['type'] == 'rss' and 'rss' in source_config:
                articles = scrape_rss_feed(source_config['rss'], source_name)
                all_articles.extend(articles)
            elif source_name == "Koch Inc News":
                articles = scrape_koch_news()
                all_articles.extend(articles)
            
            time.sleep(1)  # Be polite, wait between requests
        except Exception as e:
            print(f"❌ Error processing {source_name}: {str(e)}")
    
    print(f"\n📊 Total articles scraped: {len(all_articles)}")
    return all_articles

if __name__ == "__main__":
    # Test scraping
    articles = scrape_all_sources()
    for article in articles[:3]:
        print(f"\n📰 {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   URL: {article['url']}")
