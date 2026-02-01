# ☁️ Cloud Deployment Guide

This guide will help you deploy your Personal Intelligence Agent to the cloud so it runs 24/7.

---

## 🎯 Recommended: Railway.app (Easiest)

Railway is the easiest option with a generous free tier.

### Step 1: Prepare Your Project

1. Create a GitHub repository and push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/intelligence-agent.git
git push -u origin main
```

### Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python and deploy

### Step 3: Configure Environment Variables

In Railway dashboard:
1. Click on your project
2. Go to "Variables" tab
3. Add these variables:
   ```
   ANTHROPIC_API_KEY=your_key_here
   EMAIL_FROM=your-email@gmail.com
   EMAIL_PASSWORD=your_gmail_app_password
   PORT=5000
   ```

### Step 4: Configure Services

Railway needs two services - one for the dashboard and one for the scheduler:

1. **Service 1 (Web Dashboard)**:
   - Start Command: `gunicorn app:app`
   - This will be your public URL

2. **Service 2 (Scheduler)**:
   - Add a new service
   - Start Command: `python scheduler.py`
   - This runs in background

### Step 5: Get Your Dashboard URL

Railway will give you a URL like: `your-app.railway.app`

Visit it to see your dashboard!

---

## 🔥 Alternative: Render.com

Render offers a free tier with some limitations.

### Setup

1. Go to [render.com](https://render.com)
2. Create account
3. New → Web Service
4. Connect your GitHub repo

### Configure

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python scheduler.py` (for scheduler) or `gunicorn app:app` (for dashboard)

You'll need TWO services:
1. Web Service (dashboard) - gets a public URL
2. Background Worker (scheduler) - runs jobs

### Environment Variables

Add in Render dashboard:
```
ANTHROPIC_API_KEY=your_key
EMAIL_FROM=your_email
EMAIL_PASSWORD=your_password
```

---

## 🌊 Alternative: DigitalOcean App Platform

DigitalOcean offers $200 free credits for 60 days.

### Setup

1. Create account at [digitalocean.com](https://digitalocean.com)
2. Go to Apps
3. Create App → GitHub
4. Select repository

### Configure

**Components:**
1. Web component:
   - Type: Web Service
   - Build: `pip install -r requirements.txt`
   - Run: `gunicorn app:app --bind 0.0.0.0:8080`

2. Worker component:
   - Type: Worker
   - Build: `pip install -r requirements.txt`
   - Run: `python scheduler.py`

### Environment Variables

```
ANTHROPIC_API_KEY=your_key
EMAIL_FROM=your_email
EMAIL_PASSWORD=your_password
```

---

## 🐳 Advanced: Docker Deployment

### Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "scheduler.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - EMAIL_FROM=${EMAIL_FROM}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
    command: gunicorn app:app --bind 0.0.0.0:5000
    volumes:
      - ./intelligence_agent.db:/app/intelligence_agent.db

  scheduler:
    build: .
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - EMAIL_FROM=${EMAIL_FROM}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
    command: python scheduler.py
    volumes:
      - ./intelligence_agent.db:/app/intelligence_agent.db
```

### Deploy

```bash
docker-compose up -d
```

---

## 🔧 Alternative: VPS (DigitalOcean, Linode, AWS EC2)

If you want full control, use a VPS.

### Setup (Ubuntu 22.04)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Clone your project
git clone https://github.com/yourusername/intelligence-agent.git
cd intelligence-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
nano .env  # Edit with your credentials

# Initialize database
python database.py
```

### Create systemd Services

**Dashboard Service** (`/etc/systemd/system/intel-dashboard.service`):

```ini
[Unit]
Description=Intelligence Agent Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/intelligence-agent
Environment="PATH=/home/ubuntu/intelligence-agent/venv/bin"
ExecStart=/home/ubuntu/intelligence-agent/venv/bin/gunicorn app:app --bind 0.0.0.0:5000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Scheduler Service** (`/etc/systemd/system/intel-scheduler.service`):

```ini
[Unit]
Description=Intelligence Agent Scheduler
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/intelligence-agent
Environment="PATH=/home/ubuntu/intelligence-agent/venv/bin"
ExecStart=/home/ubuntu/intelligence-agent/venv/bin/python scheduler.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable intel-dashboard intel-scheduler
sudo systemctl start intel-dashboard intel-scheduler
sudo systemctl status intel-dashboard intel-scheduler
```

### Setup Nginx (Optional)

```bash
sudo apt install nginx -y
```

Create `/etc/nginx/sites-available/intelligence-agent`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/intelligence-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 📊 Monitoring Your Deployment

### Check Logs

**Railway:**
- View logs in Railway dashboard

**Render:**
- View logs in Render dashboard

**VPS (systemd):**
```bash
# Dashboard logs
sudo journalctl -u intel-dashboard -f

# Scheduler logs
sudo journalctl -u intel-scheduler -f
```

**Docker:**
```bash
docker-compose logs -f
```

### Health Checks

Test dashboard:
```bash
curl http://your-url.com/api/stats
```

Should return JSON with statistics.

---

## 🔐 Security Checklist

- [ ] Environment variables are set and not in code
- [ ] `.env` file is in `.gitignore`
- [ ] Using Gmail App Password (not main password)
- [ ] HTTPS enabled (use Cloudflare or Let's Encrypt)
- [ ] Firewall configured (if using VPS)
- [ ] Database file has proper permissions
- [ ] Regular backups of database

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans Start At |
|----------|-----------|---------------------|
| Railway | 500 hours/month | $5/month |
| Render | 750 hours/month | $7/month |
| DigitalOcean | $200 credit | $6/month |
| Heroku | No free tier | $7/month |
| VPS (DO/Linode) | N/A | $6/month |

**Recommendation**: Start with Railway's free tier, upgrade if needed.

---

## 🆘 Troubleshooting

### "Module not found" errors
- Ensure `requirements.txt` is correct
- Rebuild/redeploy

### Database not persisting
- Use volume mounts (Docker)
- Use persistent storage (Railway/Render provide this)

### Emails not sending
- Double-check Gmail App Password
- Verify environment variables are set correctly
- Check email in spam folder

### Dashboard not accessible
- Check if web service is running
- Verify port configuration
- Check firewall rules (VPS)

### Scheduler not running
- Verify it's set as a worker/background service
- Check logs for errors
- Ensure environment variables are available to worker

---

## 🎉 You're Live!

Once deployed, your Intelligence Agent will:
- ✅ Run 24/7 in the cloud
- ✅ Send daily emails at 8 AM
- ✅ Collect and analyze articles automatically
- ✅ Provide a beautiful dashboard accessible anywhere

Enjoy your personal intelligence system! 🚀
