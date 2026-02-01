# 🤖 Personal Intelligence Agent

Your AI-powered news and intelligence monitoring system that:
- 📡 Scrapes articles from TechCrunch, DeepMind Blog, and Koch Inc News
- 🎯 Filters content by your topics: AI, Digital Transformation, Koch Industries, Guardian Industries
- 📧 Sends daily email summaries at 8 AM
- 🌐 Beautiful web dashboard with chatbot
- 💬 Ask questions about collected articles

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Gmail account (for sending emails)
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
EMAIL_FROM=your-email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

#### 📧 Getting Gmail App Password

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Enable 2-Step Verification if not already enabled
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Generate a new app password for "Mail"
5. Copy the 16-character password (no spaces) into your `.env` file

### 3. Initialize Database

```bash
python database.py
```

### 4. Test Everything

```bash
# Test scraping
python scraper.py

# Test the daily job (won't send email unless you configure it)
python daily_job.py

# Start the dashboard
python app.py
```

Visit: `http://localhost:5000`

---

## 📅 Running the Scheduler

To run the daily job at 8 AM automatically:

```bash
python scheduler.py
```

This will:
- Run immediately once on startup
- Schedule daily runs at 8:00 AM
- Keep running until you stop it (Ctrl+C)

---

## ☁️ Cloud Deployment (Free Options)

### Option 1: Railway.app (Recommended - Easiest)

1. Create account at [railway.app](https://railway.app)
2. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```
3. Deploy:
   ```bash
   railway login
   railway init
   railway up
   ```
4. Add environment variables in Railway dashboard:
   - `ANTHROPIC_API_KEY`
   - `EMAIL_FROM`
   - `EMAIL_PASSWORD`

5. The app will automatically restart daily and run the scheduler

### Option 2: Render.com (Free Tier Available)

1. Create account at [render.com](https://render.com)
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python scheduler.py`
5. Add environment variables in Render dashboard

### Option 3: Google Cloud Run (Generous Free Tier)

```bash
# Install Google Cloud SDK
# Then deploy:
gcloud run deploy intelligence-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

Add environment variables in Cloud Run console.

### Option 4: Heroku (Free Tier Discontinued but Still an Option)

Create `Procfile`:
```
web: gunicorn app:app
worker: python scheduler.py
```

Deploy:
```bash
heroku create your-intelligence-agent
heroku config:set ANTHROPIC_API_KEY=your_key
heroku config:set EMAIL_FROM=your_email
heroku config:set EMAIL_PASSWORD=your_password
git push heroku main
heroku ps:scale worker=1
```

---

## 🖥️ Running on Your Own Computer

### Option 1: Keep Terminal Open
```bash
python scheduler.py
```
Keep the terminal window open. Not ideal for long-term use.

### Option 2: Background Process (Linux/Mac)

```bash
nohup python scheduler.py > logs.txt 2>&1 &
```

To stop:
```bash
ps aux | grep scheduler.py
kill <PID>
```

### Option 3: System Service (Linux)

Create `/etc/systemd/system/intelligence-agent.service`:

```ini
[Unit]
Description=Personal Intelligence Agent
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/project
ExecStart=/usr/bin/python3 /path/to/project/scheduler.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable intelligence-agent
sudo systemctl start intelligence-agent
sudo systemctl status intelligence-agent
```

### Option 4: Cron Job (Alternative)

```bash
crontab -e
```

Add:
```
0 8 * * * cd /path/to/project && /usr/bin/python3 daily_job.py
```

---

## 🎨 Dashboard Features

### Main Dashboard
- **Stats Bar**: Today's count, weekly count, sources, topics
- **Articles Panel**: Last 7 days of articles grouped by date
- **Chatbot Panel**: Ask questions about the articles

### Chatbot Examples
- "Summarize the latest AI developments"
- "What's happening with Koch Industries?"
- "Tell me about digital transformation articles"
- "What are the main themes this week?"

---

## ⚙️ Customization

### Change Topics
Edit `config.py`:
```python
TOPICS = [
    "Your Topic 1",
    "Your Topic 2",
    # Add more topics
]
```

### Add/Remove Websites
Edit `config.py`:
```python
WEBSITES = {
    "Site Name": {
        "url": "https://example.com",
        "rss": "https://example.com/feed",  # If RSS available
        "type": "rss"  # or "web"
    }
}
```

### Change Schedule Time
Edit `config.py`:
```python
DAILY_RUN_TIME = "08:00"  # 24-hour format
```

### Change Dashboard Days
Edit `config.py`:
```python
DASHBOARD_DAYS = 7  # Show last 7 days
```

---

## 📁 Project Structure

```
intelligence-agent/
├── app.py              # Flask web dashboard
├── scheduler.py        # Schedules daily runs
├── daily_job.py        # Main job logic
├── scraper.py          # Web scraping
├── analyzer.py         # Claude API integration
├── emailer.py          # Email sending
├── database.py         # SQLite database
├── config.py           # Configuration
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .env.example       # Example env file
├── templates/
│   └── index.html     # Dashboard HTML
└── intelligence_agent.db  # SQLite database (auto-created)
```

---

## 🔍 Troubleshooting

### Email not sending?
- Verify Gmail App Password (not regular password)
- Check `.env` file has correct credentials
- Ensure 2-Step Verification is enabled on Gmail

### No articles appearing?
- Run `python scraper.py` to test scraping
- Check if websites are accessible
- Some sites may block scraping - add headers or use different approach

### Chatbot not responding?
- Verify `ANTHROPIC_API_KEY` in `.env`
- Check API key has credits
- Ensure database has articles for context

### Dashboard not loading?
- Check if Flask is running: `python app.py`
- Try `http://0.0.0.0:5000` instead of `localhost:5000`
- Check firewall settings

---

## 🔐 Security Notes

1. **Never commit `.env` file** - it contains sensitive credentials
2. **Use App Passwords** for Gmail, not your main password
3. **Keep API keys secret** - rotate them if exposed
4. **Use HTTPS** in production deployments
5. **Set strong SECRET_KEY** in production

---

## 📊 Usage

### Manual Run
```bash
python daily_job.py
```

### Continuous Scheduling
```bash
python scheduler.py
```

### Dashboard Only
```bash
python app.py
```

---

## 🛠️ Advanced Configuration

### Rate Limiting
The scraper includes polite delays between requests. Adjust in `scraper.py`:
```python
time.sleep(1)  # Wait 1 second between requests
```

### Article Filtering
Adjust relevance threshold in `daily_job.py`:
```python
if analysis['is_relevant'] and analysis['score'] >= 5:  # Change 5 to your threshold
```

### Database Location
Change in `config.py`:
```python
DATABASE_NAME = "intelligence_agent.db"
```

---

## 📈 Monitoring

Check logs:
```bash
tail -f logs.txt  # If using nohup
journalctl -u intelligence-agent -f  # If using systemd
```

---

## 🤝 Support

- Issues with scraping specific sites? Check the site's structure
- API rate limits? Anthropic has generous limits for Sonnet
- Need to add more sources? Edit `scraper.py` and `config.py`

---

## 📝 License

Personal use project. Customize as needed!

---

## 🎉 Enjoy Your Intelligence Agent!

You now have a personal AI assistant that:
- ✅ Monitors your topics 24/7
- ✅ Sends you daily summaries
- ✅ Lets you chat about the content
- ✅ Keeps everything in one beautiful dashboard

Happy monitoring! 🚀
