from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.tasks.policies import run_policies
import atexit


def schedule(trigger=IntervalTrigger(hours=2)):
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=run_policies,
        trigger=trigger,
        replace_existing=True,
        name="Clean-up Prometheus time-series"
    )
    atexit.register(lambda: scheduler.shutdown())
