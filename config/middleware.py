import asyncio

import requests
from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.conf import settings


class WebhookMiddleware:
    endpoint_path = '/webhook-endpoint'
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        response = await self.get_response(request)
        if settings.WEBHOOK_ENABLED and request.path != self.endpoint_path:
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

                loop = asyncio.get_event_loop()
                try:
                    _response = await loop.run_in_executor(None, lambda: requests.post(url=f'{webhook_url}{self.endpoint_path}', json=payload, headers=headers))
                except BaseException as e:
                    pass
        return response
