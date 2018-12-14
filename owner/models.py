from django.db import models

from character.models import Player
from game.models import Game


class Owner(models.Model):
    """
    When a player creates a game, it has the property over that game. This
    model represents that property so that a player can administer that
    game and modify it.
    """

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="owners")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="owners")
