"""
Email module for sending daily summaries
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import config

def create_email_html(articles):
    """Create beautiful HTML email from articles"""
    
    if not articles:
        return """
        <html>
            <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">📬 Daily Intelligence Brief</h2>
                <p style="color: #7f8c8d;">No new articles found today matching your interests.</p>
            </body>
        </html>
        """
    
    # Group articles by source
    by_source = {}
    for article in articles:
        source = article.get('source', 'Unknown')
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(article)
    
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f7fa;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 20px;
            }}
            .source-section {{
                background: white;
                padding: 20px;
                margin-bottom: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .source-title {{
                color: #2c3e50;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 2px solid #667eea;
            }}
            .article {{
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 1px solid #ecf0f1;
            }}
            .article:last-child {{
                border-bottom: none;
            }}
            .article-title {{
                color: #2c3e50;
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 8px;
            }}
            .article-title a {{
                color: #667eea;
                text-decoration: none;
            }}
            .article-title a:hover {{
                text-decoration: underline;
            }}
            .summary {{
                color: #555;
                font-size: 14px;
                line-height: 1.6;
                margin-bottom: 8px;
            }}
            .topics {{
                margin-top: 8px;
            }}
            .topic-tag {{
                display: inline-block;
                background-color: #e8f4f8;
                color: #2c7a8f;
                padding: 3px 10px;
                border-radius: 12px;
                font-size: 12px;
                margin-right: 5px;
                margin-top: 5px;
            }}
            .footer {{
                text-align: center;
                color: #7f8c8d;
                font-size: 12px;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1 style="margin: 0; font-size: 28px;">📬 Daily Intelligence Brief</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">{datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        
        <p style="color: #555; font-size: 14px; margin-bottom: 20px;">
            Here's your daily summary of {len(articles)} relevant article{'s' if len(articles) != 1 else ''} 
            on AI, Digital Transformation, Koch Industries, and Guardian Industries.
        </p>
    """
    
    # Add articles grouped by source
    for source, source_articles in by_source.items():
        html += f'<div class="source-section">'
        html += f'<div class="source-title">{source} ({len(source_articles)})</div>'
        
        for article in source_articles:
            html += '<div class="article">'
            html += f'<div class="article-title"><a href="{article["url"]}">{article["title"]}</a></div>'
            html += f'<div class="summary">{article["summary"]}</div>'
            
            # Add topic tags
            if article.get('topics'):
                topics = article['topics'] if isinstance(article['topics'], list) else []
                if topics:
                    html += '<div class="topics">'
                    for topic in topics:
                        html += f'<span class="topic-tag">{topic}</span>'
                    html += '</div>'
            
            html += '</div>'
        
        html += '</div>'
    
    html += """
        <div class="footer">
            <p>🤖 Generated by your Personal Intelligence Agent</p>
            <p>View full dashboard at <a href="http://your-dashboard-url">your dashboard</a></p>
        </div>
    </body>
    </html>
    """
    
    return html

def send_daily_email(articles):
    """Send the daily summary email"""
    
    if not config.EMAIL_PASSWORD:
        print("❌ Email password not configured!")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"📬 Daily Intelligence Brief - {datetime.now().strftime('%b %d, %Y')}"
        msg['From'] = config.EMAIL_FROM
        msg['To'] = config.EMAIL_TO
        
        # Create HTML content
        html_content = create_email_html(articles)
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email
        print(f"📧 Sending email to {config.EMAIL_TO}...")
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.EMAIL_FROM, config.EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("✅ Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

if __name__ == "__main__":
    # Test email with dummy data
    test_articles = [
        {
            'title': 'Test Article',
            'url': 'https://example.com',
            'source': 'Test Source',
            'summary': 'This is a test summary.',
            'topics': ['AI', 'Digital Transformation']
        }
    ]
    send_daily_email(test_articles)
