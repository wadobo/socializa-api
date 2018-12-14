from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

from game.models import Game


class Notification(models.Model):
    """
    In this model we will save the notifications received by the users, which
    will be when: they interact with the player, receive objects or knowledge.
    """

    character_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
            limit_choices_to=models.Q(app_label='character'))
    character_id = models.PositiveIntegerField()
    character = GenericForeignKey('character_type', 'character_id')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="notifications")
    created = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=True)
    msg = models.CharField(max_length=200)
    data = JSONField(default=list)

