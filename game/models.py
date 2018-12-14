from django.db import models
from django.utils import timezone


class Preference(models.Model):
    """
    This model is directly related to Game, here we will store all the
    modifiable variables of the game (distance of vision, distance of
    iteration and visibility between players).
    """

    vision_distance = models.PositiveIntegerField(default=100)
    meeting_distance = models.PositiveIntegerField(default=20)
    visible_character = models.BooleanField(default=True)


class Game(models.Model):
    """
    this model will save title, descriptions, start_date and end_date of game.
    By other hand, a Game instance can be a template witch will be used for
    created games based in this template game. Finally, Game will have
    associatte a Preference models.
    """

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1024, blank=True, null=True)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(blank=True, null=True)
    is_template = models.BooleanField(default=True)
    preferences = models.OneToOneField(Preference, on_delete=models.CASCADE, related_name='game')
