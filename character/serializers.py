from rest_framework import serializers

from .models import Character
from .models import NPC
from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('pk', 'user')


class NPCSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPC
        fields = ('pk', 'user')


def character_serializer(character):
    if isinstance(character, Player):
        return PlayerSerializer(character).data
    elif isinstance(character, NPC):
        return NPCSerializer(character).data
    else:
        raise TypeError('Character type is unknow')

