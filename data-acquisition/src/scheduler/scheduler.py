from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

from src.scheduler.jobs import (
    bootstrap_job, 
    calendars_annual_job, 
    macro_monthly_job,
    quotes_daily_job,
    news_daily_job,
    # fundamentals_monthly_job
)

def build() -> BlockingScheduler:
    scheduler = BlockingScheduler(
        executors={'default': ThreadPoolExecutor(max_workers=1)}
    )

    scheduler.add_job(
        bootstrap_job,
        trigger='date',
        id='bootstrap_job',
        misfire_grace_time=3600,
        coalesce=True
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

    scheduler.add_job(
        macro_monthly_job,
        trigger='cron',
        day=1,
        hour=2,
        minute=0,
        id='macro_monthly_job',
        misfire_grace_time=86400,
        coalesce=True
    )

    scheduler.add_job(
        quotes_daily_job,
        trigger='cron',
        day_of_week='mon-fri',
        hour=23,
        minute=0,
        id='quotes_daily_job',
        misfire_grace_time=86400,
        coalesce=True
    )

    scheduler.add_job(
        news_daily_job,
        trigger='cron',
        hour='*/4',
        minute=0,
        id='news_daily_job',
        misfire_grace_time=3600,
        coalesce=True
    )

    # scheduler.add_job(
    #     fundamentals_monthly_job,
    #     trigger='cron',
    #     day='1',
    #     hour=0,
    #     minute=30,
    #     id='fundamentals_monthly_job',
    #     misfire_grace_time=86400,
    #     coalesce=True
    # )

    return scheduler
