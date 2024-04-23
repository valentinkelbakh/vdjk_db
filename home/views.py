import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from .models import Holiday, Project, Recipe, Webhook
from .permissions import CustomUserPermission
from .serializers import HolidaySerializer, ProjectSerializer, RecipeSerializer

logger = logging.getLogger(__name__)


class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
        CustomUserPermission,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["month", "day"]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
        CustomUserPermission,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
        CustomUserPermission,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


class SetWebhookViewSet(viewsets.ViewSet):
    def create(self, request):
        if request.method == "POST":
            if (
                request.data["webhook_url"]
                and request.data["webhook_pass"] == settings.WEBHOOK_PASS
            ):
                webhook = Webhook.objects.get_or_create()[0]
                webhook.url = request.data["webhook_url"]
                webhook.connected = True
                webhook.save()
                response = HttpResponse(
                    content="Webhook received and processed",
                    content_type="text/plain",
                )
                response["ngrok-skip-browser-warning"] = "True"
                logger.info(f'🔵 Webhook set on:\n{request.data["webhook_url"]}\n')
                return response
        return HttpResponseBadRequest("Invalid")


class CheckWebhookViewSet(viewsets.ViewSet):
    def create(self, request):
        if request.method == "POST":
            webhook = Webhook.objects.get_or_create()[0]
            if (
                request.data["webhook_pass"] == settings.WEBHOOK_PASS
                and webhook.connected
                and request.data["webhook_url"] == webhook.url
            ):
                response = HttpResponse(
                    content="Webhook is active",
                    content_type="text/plain",
                )
                response["ngrok-skip-browser-warning"] = "True"
                logger.info(
                    f'🔵 Webhook connection confirmed:\n{request.data["webhook_url"]}\n'
                )
                return response
        return HttpResponseBadRequest("Invalid")
