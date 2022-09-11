from apscheduler.schedulers.background import BackgroundScheduler
from .models import ChannelData


def start(job, interval):
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, "interval", minutes=interval)
    scheduler.start()


def delete_channel_data():
    ChannelData.delete_scheduled_records()


__all__ = ["start", "delete_channel_data"]