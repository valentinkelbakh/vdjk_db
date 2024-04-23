from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from home import views

admin.site.site_url = ""
router = routers.DefaultRouter()
router.register(r"holidays", views.HolidayViewSet)
router.register(r"projects", views.ProjectViewSet)
router.register(r"recipes", views.RecipeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.WEBHOOK:
    urlpatterns = urlpatterns + [
        path(
            "set-webhook/",
            views.SetWebhookViewSet.as_view({"post": "create", "get": "create"}),
            name="set-webhook",
        ),
        path(
            "check-webhook/",
            views.CheckWebhookViewSet.as_view({"post": "create"}),
            name="check-webhook",
        ),
    ]
