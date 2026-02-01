"""
Configuration file for Personal Intelligence Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Topics you're interested in
TOPICS = [
    "AI",
    "Digital Transformation",
    "Koch Industries",
    "Guardian Industries"
]

# Websites to monitor
WEBSITES = {
    "TechCrunch": {
        "url": "https://techcrunch.com",
        "rss": "https://techcrunch.com/feed/",
        "type": "rss"
    },
    "Koch Inc News": {
        "url": "https://www.kochinc.com/newsroom",
        "type": "web"
    },
    "DeepMind Blog": {
        "url": "https://deepmind.google/blog/",
        "rss": "https://deepmind.google/blog/rss.xml",
        "type": "rss"
    }
}

# Email configuration
EMAIL_FROM = os.getenv("EMAIL_FROM", "your-email@gmail.com")
EMAIL_TO = "rkarthikn2020@gmail.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Gmail app password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Claude API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Schedule time (24-hour format)
DAILY_RUN_TIME = "08:00"

# Database
DATABASE_NAME = "intelligence_agent.db"

# Days to keep in dashboard
DASHBOARD_DAYS = 7

# Flask app settings
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
DEBUG = False
PORT = 5000
