import time
import logging
import json
import requests
from django.conf import settings


class WebhookMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            webhook_url = settings.WEBHOOK_URL

            payload = {
                "content": settings.WEBHOOK_PASS
            }

            headers = {
                "Content-Type": "application/json"
            }

            _response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        return response
