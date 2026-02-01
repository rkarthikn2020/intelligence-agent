"""
Daily job that scrapes, analyzes, and emails summaries
"""
from datetime import datetime
import scraper
import analyzer
import database
import sendgrid_emailer as emailer
import config

def run_daily_job():
    """Main job that runs daily at scheduled time"""
    
    print(f"\n{'='*60}")
    print(f"🚀 Starting Daily Intelligence Agent Job")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # Step 1: Scrape all sources
    print("📡 Step 1: Scraping articles from sources...")
    raw_articles = scraper.scrape_all_sources()
    
    if not raw_articles:
        print("⚠️  No articles found. Ending job.")
        return
    
    # Step 2: Analyze and filter articles
    print(f"\n🔬 Step 2: Analyzing {len(raw_articles)} articles...")
    relevant_articles = []
    
    for i, article in enumerate(raw_articles, 1):
        print(f"  Analyzing {i}/{len(raw_articles)}: {article['title'][:60]}...")
        
        analysis = analyzer.analyze_article(
            article['title'],
            article.get('content', article.get('summary', '')),
            article['url']
        )
        
        if analysis['is_relevant'] and analysis['score'] >= 5:
            # Save to database
            article_id = database.save_article(
                title=article['title'],
                url=article['url'],
                source=article['source'],
                summary=analysis['summary'],
                topics=analysis['topics'],
                content=article.get('content', ''),
                published_date=article.get('published', '')
            )
            
            if article_id:
                relevant_articles.append({
                    'title': article['title'],
                    'url': article['url'],
                    'source': article['source'],
                    'summary': analysis['summary'],
                    'topics': analysis['topics'],
                    'score': analysis['score']
                })
                print(f"    ✅ Relevant (score: {analysis['score']}) - Topics: {', '.join(analysis['topics'])}")
        else:
            print(f"    ⏭️  Skipped (not relevant or low score: {analysis['score']})")
    
    print(f"\n📊 Found {len(relevant_articles)} relevant articles")
    
    # Step 3: Send email summary
    if relevant_articles:
        print("\n📧 Step 3: Sending email summary...")
        success = emailer.send_daily_email(relevant_articles)
        if success:
            print("✅ Email sent successfully!")
        else:
            print("❌ Failed to send email")
    else:
        print("\n📧 Step 3: No relevant articles to email")
    
    print(f"\n{'='*60}")
    print(f"✅ Daily job completed!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # Initialize database
    database.init_db()
    # Run the job
    run_daily_job()
