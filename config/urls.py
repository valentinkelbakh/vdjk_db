from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from home import views

router = routers.DefaultRouter()
router.register(r'holidays', views.HolidayViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'set-webhook', views.WebhookViewSet, basename='set-webhook')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
