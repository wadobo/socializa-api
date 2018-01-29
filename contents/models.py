from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone

from game.models import Game


class Content(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="contents")
    content_type = models.ForeignKey(ContentType,
            on_delete=models.CASCADE,
            related_name="content_of",
            limit_choices_to=models.Q(app_label='character') | models.Q(app_label='things'))
    content_id = models.PositiveIntegerField()
    content = GenericForeignKey('content_type', 'content_id')
    position = models.PointField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
