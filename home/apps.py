import logging

import requests
from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        if settings.WEBHOOK and not settings.webhook_connected:
            from .models import Webhook

            webhook = Webhook.objects.first()
            if not webhook:
                logger.info("No last Webhook URL")
                return
            url = webhook.url
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    settings.webhook_connected = True
                    settings.WEBHOOK_URL = url
                    logger.info(f"Webhook set on:\n{url}\n")
                else:
                    webhook.delete()
                    logger.info(f"Last Webhook URL is no longer available: {url}")
            except Exception as e:
                logger.error(f"Error setting webhook: {e}")
        return
