import schedule
import time
import asyncio
from loguru import logger
from main import run_pipeline

def job():
    logger.info("Running scheduled ingestion job...")
    # Passing empty query to just trigger ingestion
    asyncio.run(run_pipeline(query=""))

def start_scheduler():
    logger.info("Scheduler started. Running every 6 hours.")
    # Run once immediately
    job()
    
    schedule.every(6).hours.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_scheduler()
