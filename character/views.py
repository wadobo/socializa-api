from django.db.utils import IntegrityError
from rest_framework import generics
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_409_CONFLICT as ST_409
)
from rest_framework.response import Response

from .models import Player
from .models import NPC
from .serializers import character_serializer
from .serializers import PlayerSerializer
from .serializers import NPCSerializer


class CharacterListCreate(generics.ListCreateAPIView):
    serializer_class = PlayerSerializer

    def create(self, request, version, *args, **kwargs):
        character_type = request.data.pop('type')
        try:
            character = globals()[character_type].create(**request.data)
            character.save()
        except IntegrityError:
            return Response('Error try to create character', status=ST_409)

        return Response('Character created', status=ST_201)

    def list(self, request, version, *args, **kwargs):
        pc = Player.objects.filter(**request.data)
        npc = NPC.objects.filter(**request.data)
        characters = PlayerSerializer(pc, many=True).data + NPCSerializer(npc, many=True).data
        return Response(characters)


class CharacterDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlayerSerializer

    def destroy(self, request, version, pk, *args, **kwargs):
        character_type = request.data.get('type', None)
        try:
            character = globals()[character_type].objects.get(pk=pk)
            character.delete()
        except:
            return Response(status=ST_400)
        return Response(status=ST_204)


    def update(self, request, version, pk, *args, **kwargs):
        character_type = request.data.pop('type', None)
        if not character_type:
            return Response(status=ST_400)
        character = globals()[character_type].objects.filter(pk=pk)
        if not character.update(**request.data):
            return Response(status=ST_400)
        return Response(character_serializer(character.first()))

    def retrieve(self, request, version, pk, *args, **kwargs):
        character_type = request.query_params.get('type', None)
        if not character_type:
            return Response(status=ST_400)
        try:
            character = globals()[character_type].objects.get(pk=pk)
        except:
            return Response(status=ST_400)
        return Response(character_serializer(character))

