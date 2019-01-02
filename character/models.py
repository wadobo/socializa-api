from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


# User email will be unique
User._meta.get_field('email')._unique = True


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


class NPC(Character):
    """
    This model represents a non-real player, it will be controlled by an AI or
    actor.
    """


@receiver(post_delete, sender=NPC)
@receiver(post_delete, sender=Player)
def post_delete_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
