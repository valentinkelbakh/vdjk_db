import json
from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import *


class HolidaySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    date_raw = serializers.SerializerMethodField()

    class Meta:
        model = Holiday
        fields = '__all__'

    def get_date(self, obj):
        return f"{obj.get_month_display()} {obj.day}"

    def get_date_raw(self, obj):
        return f"{obj.month:02d}-{obj.day:02d}"

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'