from rest_framework import serializers

from .models import Character
from .models import NPC
from .models import Player


class CharacterSerializer(serializers.ModelSerializer):

    class Meta:
        abstract = True


class PlayerSerializer(CharacterSerializer):

    class Meta:
        model = Player
        fields = '__all__'


class NPCSerializer(CharacterSerializer):

    class Meta:
        model = NPC
        fields = '__all__'


def character_serializer(character):
    if isinstance(character, Player):
        return PlayerSerializer(character).data
    elif isinstance(character, NPC):
        return NPCSerializer(character).data
    else:
        raise TypeError('Character type is unknow')

