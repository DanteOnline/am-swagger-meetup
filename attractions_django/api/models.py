from django.db import models


class Attraction(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_popular = models.BooleanField(default=False)
    language = models.CharField(max_length=50)  # ISO: "ru", "en", etc.
    tags = models.JSONField(blank=True, default=list)  # Список тегов: ["museum", "family"]

    # def __str__(self):
    #     return f"{self.name} ({self.city})"
