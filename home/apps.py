from django.apps import AppConfig
from django.conf import settings
import requests
class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        from .models import Webhook
        try:
            url = Webhook.objects.get_or_create()[0].url
            response = requests.get(url)
            if response.status_code == 200:
                settings.WEBHOOK_ENABLED = True
                settings.WEBHOOK_URL = url
                print(f'Webhook set on:\n{url}\n')
            return
        except Exception as e:
            return
