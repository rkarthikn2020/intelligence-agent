# ⚡ Quick Start Guide

Get your Intelligence Agent running in 5 minutes!

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Anthropic API Key** ([Get free key](https://console.anthropic.com/))
3. **Gmail account** for sending emails

---

## 🚀 5-Minute Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Credentials

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` file with your credentials:
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
EMAIL_FROM=youremail@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
```

**Getting Gmail App Password:**
1. Go to [Google Account](https://myaccount.google.com/)
2. Enable "2-Step Verification"
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Generate password for "Mail"
5. Copy the 16-character password (no spaces)

### 3. Initialize Database

```bash
python database.py
```

### 4. Test Everything

```bash
# Test scraping (should show found articles)
python scraper.py

# Test the full pipeline (scrape + analyze + email)
python daily_job.py
```

### 5. Start the Dashboard

```bash
python app.py
```

Visit: **http://localhost:5000**

### 6. Enable Daily Automation

In a new terminal:
```bash
python scheduler.py
```

This runs the daily job at 8 AM and keeps the system running.

---

## 🎯 What It Does

✅ **Every day at 8 AM:**
- Scrapes TechCrunch, DeepMind Blog, Koch Inc News
- Filters for your topics (AI, Digital Transformation, Koch Industries, Guardian Industries)
- Analyzes relevance using Claude AI
- Sends beautiful email summary to rkarthikn2020@gmail.com
- Stores articles in database

✅ **Dashboard (localhost:5000):**
- View last 7 days of articles
- See statistics
- Chat with AI about the articles
- Search through collected content

---

## 💡 Quick Commands

```bash
# Run job once (test)
python daily_job.py

# Start scheduler (daily at 8 AM)
python scheduler.py

# Start dashboard only
python app.py

# Check database
python -c "import database; print(len(database.get_recent_articles()))"
```

---

## ⚙️ Customization

### Change Email Time

Edit `config.py`:
```python
DAILY_RUN_TIME = "08:00"  # Change to your preferred time
```

### Add More Topics

Edit `config.py`:
```python
TOPICS = [
    "AI",
    "Digital Transformation",
    "Koch Industries",
    "Guardian Industries",
    "Your New Topic"  # Add here
]
```

### Change Email Recipient

Edit `config.py`:
```python
EMAIL_TO = "newemail@example.com"
```

---

## 🐛 Troubleshooting

### No articles appearing?
```bash
# Test scraping
python scraper.py

# Check if articles are being saved
python -c "import database; print(database.get_recent_articles())"
```

### Email not sending?
- Verify Gmail App Password (not regular password)
- Check `.env` file credentials
- Test: `python emailer.py`

### Dashboard not loading?
- Is Flask running? Check terminal output
- Try: `http://127.0.0.1:5000` instead of `localhost`
- Check firewall settings

### Chatbot not responding?
- Verify `ANTHROPIC_API_KEY` in `.env`
- Check API credits at [console.anthropic.com](https://console.anthropic.com/)
- Ensure database has articles

---

## 🌐 Deploy to Cloud

Want it running 24/7? See **DEPLOYMENT.md** for:
- Railway.app (easiest, free)
- Render.com (free tier)
- DigitalOcean (free credits)
- VPS setup

---

## 📚 Next Steps

1. ✅ Get it running locally
2. ✅ Customize topics and sources
3. ✅ Test the email and dashboard
4. ✅ Deploy to cloud for 24/7 operation

---

## 🎉 You're Ready!

Your Personal Intelligence Agent is now:
- 📡 Monitoring your topics
- 🤖 Analyzing with AI
- 📧 Sending daily summaries
- 🌐 Accessible via dashboard

Enjoy! 🚀

---

**Need Help?**
- Check README.md for detailed docs
- See DEPLOYMENT.md for cloud setup
- Review config.py for all settings
