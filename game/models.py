from django.db import models
from django.utils import timezone


class Preference(models.Model):
    vision_distance = models.PositiveIntegerField(default=100)
    meeting_distance = models.PositiveIntegerField(default=20)
    visible_character = models.BooleanField(default=True)


class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1024, blank=True, null=True)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(blank=True, null=True)
    is_template = models.BooleanField(default=True)
    preferences = models.OneToOneField(Preference, on_delete=models.CASCADE, related_name='game')
