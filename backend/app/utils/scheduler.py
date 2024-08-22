# utils/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from app.services.data_acquisition import DataAcquisition
from app.database import SessionLocal

def fetch_data_job():
    db = SessionLocal()
    try:
        api_key = "Q05ZiddarLQF3oSkvQbOlSOVj59FyqcU8iYpWNvr"
        search_terms = ["Ruto"]

        acquisition = DataAcquisition(api_key, search_terms)
        acquisition.fetch_and_save_articles(db)
    finally:
        db.close()

def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_data_job, 'cron', hour=3, minute=0)  # Run the job every day at 3:00 AM
    scheduler.start()
