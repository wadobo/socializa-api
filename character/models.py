from django.db import models
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
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


@receiver(post_save, sender=User)
def post_create_user(sender, instance, created, **kwargs):
    if created:
        player, created = Player.objects.get_or_create(user=instance)
        if created:
            player.save()


@receiver(post_delete, sender=NPC)
@receiver(post_delete, sender=Player)
def post_delete_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
