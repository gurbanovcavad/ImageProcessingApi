from django.apps import AppConfig
import os
from django.conf import settings


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def ready(self):
        os.makedirs("/images/input/", exist_ok=True)
        os.makedirs("/images/output/", exist_ok=True)