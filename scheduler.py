"""
Scheduler for running the daily job at 8 AM. Adding new
Adding comments
"""
import schedule
import time
from datetime import datetime
import daily_job
import config
import database

def job():
    """Wrapper for the daily job"""
    print(f"\n⏰ Scheduled job triggered at {datetime.now()}")
    daily_job.run_daily_job()

def run_scheduler():
    """Run the scheduler continuously"""
    
    print("🤖 Personal Intelligence Agent Scheduler Started")
    print(f"⏰ Scheduled to run daily at {config.DAILY_RUN_TIME}")
    print(f"📅 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nPress Ctrl+C to stop\n")
    
    # Initialize database
    database.init_db()
    
    # Schedule the job
    schedule.every().day.at(config.DAILY_RUN_TIME).do(job)
    
    # Run immediately once at startup (optional - comment out if you don't want this)
    print("🚀 Running initial job at startup...")
    job()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("\n\n👋 Scheduler stopped by user")
