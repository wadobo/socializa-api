from django.db import models


class Thing(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1024, blank=True, null=True)

    class Meta:
        abstract = True


class Item(Thing):
    pickable = models.BooleanField(default=True)
    shareable = models.BooleanField(default=True)
    consumable = models.BooleanField(default=False)


class Knowledge(Thing):
    shareable = models.BooleanField(default=True)


class Rol(Thing):
    pass


THING_TYPES = models.Q(app_label='thing', model='Item')
THING_TYPES |= models.Q(app_label='thing', model='Knowledge')
THING_TYPES |= models.Q(app_label='thing', model='Rol')
