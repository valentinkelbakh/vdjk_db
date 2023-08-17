from django.contrib import admin
from .models import Holiday, Project, Recipe

# Register your models here.

admin.site.register(Holiday)
admin.site.register(Project)
admin.site.register(Recipe)