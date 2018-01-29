from django.db import models

from character.models import Player
from game.models import Game


class Owner(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="owners")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="owners")
