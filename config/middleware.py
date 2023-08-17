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
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            webhook_url = settings.WEBHOOK_URL

            payload = {
                "content": settings.WEBHOOK_PASS
            }

            headers = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }

            try:
                _response = requests.post(webhook_url, data=payload, headers=headers)
            except Exception as ConnectionError:
                pass
        return response
