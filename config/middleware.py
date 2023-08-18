import time
import logging
import json
import requests
from django.conf import settings
from requests.exceptions import ConnectionError

class WebhookMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.WEBHOOK_ENABLED:            
            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                webhook_url = settings.WEBHOOK_URL

                payload = {
                    "content": settings.WEBHOOK_PASS
                }

                headers = {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "ngrok-skip-browser-warning": "True"
                }

                try:
                    _response = requests.post(f'{webhook_url}/webhook-endpoint', json=payload, headers=headers)
                except Exception as ConnectionError:
                    pass
        return response
