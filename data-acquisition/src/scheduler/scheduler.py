from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

from .jobs import bootstrap_job, calendars_annual_job

def build() -> BlockingScheduler:
    scheduler = BlockingScheduler(
        executors={'default': ThreadPoolExecutor(max_workers=1)}
    )

    scheduler.add_job(
        calendars_annual_job,
        trigger='cron',
        month=1,
        day=1,
        hour=0,
        minute=30,
        id='calendars_annual_job',
        misfire_grace_time=86400,
        coalesce=True
    )

    calendars_annual_job()

    return scheduler
