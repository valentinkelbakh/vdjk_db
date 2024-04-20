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
        if (
            settings.WEBHOOK
            and settings.webhook_connected
            and request.path != self.endpoint_path
        ):
            if (
                request.method in ["POST", "PUT", "PATCH", "DELETE"]
                and "/home" in request.path
            ):
                payload = {
                    "webhook_pass": settings.WEBHOOK_PASS,
                    "update_subject": request.resolver_match.func.model_admin.model._meta.verbose_name_plural.__str__(),
                }

                headers = {
                    "Content-Type": "application/json",
                    "Accept": "text/plain",
                    "Access-Control-Allow-Origin": "*",
                    "ngrok-skip-browser-warning": "True",
                }

                loop = asyncio.get_event_loop()

                for i in range(3):
                    try:
                        webhook_response = await loop.run_in_executor(
                            executor=None,
                            func=lambda: requests.post(
                                url=f"{settings.WEBHOOK_URL}{self.endpoint_path}",
                                json=payload,
                                headers=headers,
                            ),
                        )
                        if webhook_response.status_code == 200:
                            break
                    except BaseException as e:
                    if i == 2:
                        webhook = Webhook.objects.first()
                        webhook.delete()
                        )
                        settings.webhook_connected = False
                        break
                    await asyncio.sleep(2)

        return response
