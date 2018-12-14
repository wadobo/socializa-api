from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from game.models import Game


class Property(models.Model):
    """
    Represents the ownership relationship between things and players or things
    and NPCs.
    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="properties")
    character_type = models.ForeignKey(ContentType,
            on_delete=models.CASCADE,
            related_name="character_of",
            limit_choices_to=models.Q(app_label='character'))

    character_id = models.PositiveIntegerField()
    character = GenericForeignKey('character_type', 'character_id')
    thing_type = models.ForeignKey(ContentType,
            on_delete=models.CASCADE,
            related_name="thing_of",
            limit_choices_to=models.Q(app_label='things'))
    thing_id = models.PositiveIntegerField()
    thing = GenericForeignKey('thing_type', 'thing_id')
    created = models.DateTimeField(default=timezone.now)
