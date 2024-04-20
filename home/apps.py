import requests
from django.apps import AppConfig
from django.conf import settings


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        if settings.WEBHOOK and not settings.webhook_connected:
            from .models import Webhook

            webhook = Webhook.objects.first()
            if not webhook:
                return
            url = webhook.url
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    settings.webhook_connected = True
                    settings.WEBHOOK_URL = url
                else:
                    webhook.delete()
            except Exception as e:
        return
