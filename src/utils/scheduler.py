from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.tasks.policies import task_run_policies
import atexit


def schedule():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=task_run_policies,
        trigger=IntervalTrigger(minutes=20),
        name='Schedule task "cleanup time-series" every 20 minutes',
        replace_existing=True
    )
    atexit.register(lambda: scheduler.shutdown())
