from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models


class Character(models.Model):
    """
    This model will be used for the characters of the game, where we will
    distinguish between two classes, Player and NPC.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE,
            related_name='%(app_label)s_%(class)s')

    class Meta:
        abstract = True

    @classmethod
    def create(cls, email, password):
        user = User.objects.create_user(email, email, password)
        user.save()
        player = cls(user=user)
        player.save()
        return player

    def __str__(self):
        return self.user.username


class Player(Character):
    """
    This model represents a real person in the game. A player will have a
    related user to play with.
    """

    pass


class NPC(Character):
    """
    This model represents a non-real player, it will be controlled by an AI or
    actor.
    """

    pass
