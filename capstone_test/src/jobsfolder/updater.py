from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api

def start():
	scheduler = BackgroundScheduler(timezone='Asia/Manila')
	#scheduler.add_job(schedule_api, 'interval', seconds=300)
	scheduler.add_job(schedule_api, 'cron', day_of_week='mon-fri', hour=15, minute=8,)
	scheduler.start()

	