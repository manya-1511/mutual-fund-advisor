# Backend/scheduler.py
import schedule
import time
from fetch_amfi_data import fetch_previous_day_amfi_nav

def job():
    print("\n⏰ Running scheduled AMFI data fetch...")
    fetch_previous_day_amfi_nav()

# Schedule to run every day at 6:00 PM
schedule.every().day.at("18:00").do(job)

print("📅 Scheduler started... will run every day at 6:00 PM.")
print("Press Ctrl+C to stop.\n")

while True:
    schedule.run_pending()
    time.sleep(60)
