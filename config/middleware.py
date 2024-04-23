import asyncio, aiohttp
import logging

from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.conf import settings

from home.models import Webhook

logger = logging.getLogger(__name__)


class WebhookMiddleware:
    endpoint_path = "/webhook-endpoint"
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        self.webhook = Webhook.objects.get_or_create()[0]
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        response = await self.get_response(request)
        if (
            settings.WEBHOOK
            and self.webhook.connected
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
                    url = f"{self.webhook.url}{self.endpoint_path}"
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.post(
                                url, json=payload, headers=headers
                            ) as _response:
                                webhook_response_text = await _response.text()
                                webhook_response_status = _response.status
                        logger.info(f"🔵 Webhook response: {webhook_response_text}")
                        if webhook_response_status == 200:
                            break
                        logger.warning(
                            f"🔵 Webhook not delivered: {webhook_response_status}"
                        )
                    except BaseException as e:
                        logger.error(f"🔵 Error sending webhook: {e}")
                    if i == 2:
                        logger.info(
                            f"🔵 Webhook URL is no longer available: {self.webhook.url}"
                        )
                        self.webhook.url = ""
                        self.webhook.connected = False
                        self.webhook.save()
                        break
                    logger.info(f"🔵 Retrying webhook in 2 seconds...")
                    await asyncio.sleep(2)

        return response
