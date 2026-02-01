# 📁 Project Structure

```
intelligence-agent/
│
├── 📄 Core Application Files
│   ├── app.py                  # Flask web dashboard server
│   ├── scheduler.py            # Schedules daily runs at 8 AM
│   ├── daily_job.py            # Main job: scrape → analyze → email
│   ├── scraper.py              # Web scraping logic
│   ├── analyzer.py             # Claude AI integration
│   ├── emailer.py              # Email sending functionality
│   ├── database.py             # SQLite database operations
│   └── config.py               # Configuration settings
│
├── 🌐 Web Dashboard
│   └── templates/
│       └── index.html          # Beautiful dashboard UI with chatbot
│
├── 🎨 Static Assets (empty - can add CSS/JS here)
│   └── static/
│
├── ⚙️ Configuration
│   ├── .env.example            # Example environment variables
│   ├── .gitignore              # Git ignore rules
│   ├── requirements.txt        # Python dependencies
│   └── Procfile                # For Heroku/Railway deployment
│
├── 📚 Documentation
│   ├── README.md               # Complete documentation
│   ├── QUICKSTART.md           # 5-minute setup guide
│   ├── DEPLOYMENT.md           # Cloud deployment guide
│   └── PROJECT_STRUCTURE.md    # This file!
│
├── 🚀 Helper Scripts
│   └── run.sh                  # Interactive startup script
│
└── 💾 Generated Files (created when you run)
    ├── .env                    # Your credentials (create from .env.example)
    └── intelligence_agent.db   # SQLite database (auto-created)
```

---

## 📄 File Descriptions

### Core Application

**app.py** (Flask Web Server)
- Serves the dashboard at http://localhost:5000
- Provides REST API endpoints:
  - `/api/articles` - Get recent articles
  - `/api/chat` - Chatbot endpoint
  - `/api/search` - Search articles
  - `/api/stats` - Dashboard statistics

**scheduler.py** (Job Scheduler)
- Runs continuously
- Executes daily_job.py at 8:00 AM daily
- Can run job immediately on startup

**daily_job.py** (Main Pipeline)
- Scrapes articles from all sources
- Analyzes each article with Claude AI
- Filters by relevance and topics
- Saves to database
- Sends email summary

**scraper.py** (Web Scraping)
- Fetches from TechCrunch RSS
- Fetches from DeepMind Blog RSS
- Scrapes Koch Inc newsroom
- Returns standardized article data

**analyzer.py** (AI Analysis)
- Uses Claude API to analyze articles
- Determines relevance to your topics
- Generates 1-2 sentence summaries
- Extracts relevant topics
- Powers the chatbot responses

**emailer.py** (Email Sending)
- Creates beautiful HTML emails
- Groups articles by source
- Adds topic tags
- Sends via Gmail SMTP

**database.py** (Data Storage)
- SQLite database operations
- Stores articles with metadata
- Provides query functions
- Handles date filtering

**config.py** (Settings)
- Topics: AI, Digital Transformation, Koch Industries, Guardian Industries
- Websites: TechCrunch, DeepMind, Koch Inc
- Email settings
- Schedule time (8 AM)
- All configurable parameters

---

## 🎨 Frontend

**templates/index.html** (Dashboard UI)
- Modern, beautiful design
- Multi-pane layout:
  1. Stats bar (today, week, sources, topics)
  2. Articles panel (scrollable, 7 days)
  3. Chatbot panel (ask questions)
- Real-time updates
- Responsive design
- Dark theme with blue accents

---

## ⚙️ Configuration Files

**.env.example**
- Template for your credentials
- Copy to `.env` and fill in:
  - ANTHROPIC_API_KEY
  - EMAIL_FROM
  - EMAIL_PASSWORD

**requirements.txt**
- All Python dependencies
- Flask for web server
- BeautifulSoup for scraping
- Anthropic for Claude API
- And more...

**Procfile**
- For cloud deployment
- Defines web and worker processes

**.gitignore**
- Excludes sensitive files from git
- Ignores .env, database, logs

---

## 📚 Documentation

**README.md** - Complete documentation
- Installation guide
- Configuration steps
- Usage instructions
- Troubleshooting
- All features explained

**QUICKSTART.md** - Get started in 5 minutes
- Minimal steps to run
- Quick testing
- Common commands

**DEPLOYMENT.md** - Cloud deployment
- Railway.app (easiest)
- Render.com
- DigitalOcean
- VPS setup
- Docker configuration

---

## 🚀 Helper Scripts

**run.sh** (Interactive Startup)
- Checks prerequisites
- Sets up virtual environment
- Installs dependencies
- Interactive menu:
  1. Run job once
  2. Start scheduler
  3. Start dashboard
  4. Run everything

---

## 🔄 Data Flow

```
1. Scheduler (runs at 8 AM)
   ↓
2. Daily Job starts
   ↓
3. Scraper fetches articles
   ↓
4. Analyzer (Claude AI)
   ├─→ Determines relevance
   ├─→ Extracts topics
   └─→ Generates summary
   ↓
5. Database saves articles
   ↓
6. Emailer sends summary
   ↓
7. Dashboard displays articles
   ↓
8. Chatbot answers questions
```

---

## 📊 API Endpoints

```
GET  /                    # Dashboard homepage
GET  /api/articles        # Get recent articles (JSON)
POST /api/chat           # Chatbot endpoint (JSON)
GET  /api/search?q=...   # Search articles (JSON)
GET  /api/stats          # Dashboard statistics (JSON)
```

---

## 💾 Database Schema

```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    source TEXT NOT NULL,
    summary TEXT,
    topics TEXT,              -- JSON array
    content TEXT,
    published_date TEXT,
    scraped_date TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎯 Key Features

✅ **Automated Daily Scraping** - Runs at 8 AM
✅ **AI-Powered Analysis** - Claude filters and summarizes
✅ **Beautiful Emails** - HTML formatted with topics
✅ **Interactive Dashboard** - Multi-pane, responsive
✅ **Smart Chatbot** - Ask questions about articles
✅ **Persistent Storage** - SQLite database
✅ **Cloud Ready** - Easy deployment options
✅ **Customizable** - Topics, sources, schedule

---

## 🔧 Customization Points

Want to customize? Edit these:

**Topics** → `config.py` (TOPICS list)
**Sources** → `config.py` (WEBSITES dict) + `scraper.py`
**Schedule** → `config.py` (DAILY_RUN_TIME)
**Email recipient** → `config.py` (EMAIL_TO)
**Dashboard days** → `config.py` (DASHBOARD_DAYS)
**UI styling** → `templates/index.html` (CSS in <style>)
**Analysis logic** → `analyzer.py` (prompts, scoring)

---

## 🎉 Ready to Use!

Everything is organized and ready to run. Start with **QUICKSTART.md** for immediate setup!
