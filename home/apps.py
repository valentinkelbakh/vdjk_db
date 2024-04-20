import requests
from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        if settings.WEBHOOK and not settings.webhook_connected:
            from .models import Webhook
            webhook = Webhook.objects.first()
            if not webhook:
                logging.info("No last Webhook URL")
                return
            url = webhook.url
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    settings.webhook_connected = True
                    settings.WEBHOOK_URL = url
                else:
                    logging.info(f"Last Webhook URL is no longer available: {url}")
