from rest_framework import serializers

from .models import Character
from .models import NonPlayerCharacter as NPC
from .models import PlayerCharacter as PC


class PCSerializer(serializers.Serializer):
    class Meta:
        model = PC
        fields = ('pk', 'user', 'position')


class NPCSerializer(serializers.Serializer):
    class Meta:
        model = NPC
        fields = ('pk', 'user', 'position')


def character_serializer(character):
    if isinstance(character, PC):
        return PCSerializer(character).data
    elif isinstance(character, NPC):
        return NPCSerializer(character).data
    else:
        raise TypeError('Character type is unknow')

