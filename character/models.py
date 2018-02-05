from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models


class Character(models.Model):
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
    pass


class NPC(Character):
    pass
