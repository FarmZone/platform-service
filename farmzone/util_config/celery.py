from __future__ import absolute_import, unicode_literals
import os
import celery
from bugsnag.celery import connect_failure_handler
connect_failure_handler()

# set the default Django settings module for the 'celery' program.
# always default to local. QA/Production must be explicit
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmzone.settings.local')

app = celery.Celery('farmzone')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
