# chatapp_backend/chatapp_with_videocalling/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp_with_videocalling.settings")

app = Celery("chatapp_with_videocalling")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
