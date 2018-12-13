from django.db import models


class Thing(models.Model):
    """
    A thing is any detail that may appear in the game. A player can interact
    with it or be added to the player. There's 3 types: Item, Knowledge y Rol.
    """

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1024, blank=True, null=True)

    class Meta:
        abstract = True


class Item(Thing):
    """
    It will represent an object within the game, for example: a stone, a cane,
    a book or a bush.
    """

    pickable = models.BooleanField(default=True)
    shareable = models.BooleanField(default=True)
    consumable = models.BooleanField(default=False)


class Knowledge(Thing):
    """
    It will be something that the player learns, a knowledge as for example: to
    know how to open a door with a picklock, or to know how to climb. This will
    help us to have certain knowledge, to be able to do things that we couldn't
    do if we didn't have them.
    """
    shareable = models.BooleanField(default=True)


class Rol(Thing):
    """
    Similar to the conomiento, although more specifically associated with a
    role of the character, to give him a prefession or class, with which he
    will be able to do certain types of things that with another Role would be
    impossible. For example: someone with the Role of Thief can steal or open
    doors and someone with the Role of Doctor can heal.
    """
    pass


THING_TYPES = models.Q(app_label='thing', model='Item')
THING_TYPES |= models.Q(app_label='thing', model='Knowledge')
THING_TYPES |= models.Q(app_label='thing', model='Rol')
