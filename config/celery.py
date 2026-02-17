import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('rental_management')

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all apps
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'generate-monthly-bills': {
        'task': 'apps.billing.tasks.generate_monthly_bills',
        'schedule': crontab(hour=0, minute=0, day_of_month=1),  # First day of every month
    },
    'check-overdue-bills': {
        'task': 'apps.billing.tasks.check_overdue_bills',
        'schedule': crontab(hour=9, minute=0),  # Daily at 9 AM
    },
    'cleanup-expired-tokens': {
        'task': 'apps.accounts.tasks.cleanup_expired_tokens',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
