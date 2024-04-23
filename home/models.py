from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Holiday(models.Model):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    MONTH_CHOICES = (
        (JANUARY, "Январь"),
        (FEBRUARY, "Февраль"),
        (MARCH, "Март"),
        (APRIL, "Апрель"),
        (MAY, "Май"),
        (JUNE, "Июнь"),
        (JULY, "Июль"),
        (AUGUST, "Август"),
        (SEPTEMBER, "Сентябрь"),
        (OCTOBER, "Октябрь"),
        (NOVEMBER, "Ноябрь"),
        (DECEMBER, "Декабрь"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    day = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(31)], blank=True, null=True
    )
    month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True)
    link = models.URLField()

    @property
    def date(self):
        return f"{self.get_month_display()} {self.day}"

    @property
    def date_raw(self):
        return f"{self.month:02d}-{self.day:02d}"

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["month", "day"]


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    img_link = models.URLField()
    apply_link = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    img_link = models.URLField()
    recipe_link = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class Webhook(models.Model):
    url = models.URLField(blank=True, null=True)
    connected = models.BooleanField(default=False)
