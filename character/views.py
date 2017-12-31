from django.db.utils import IntegrityError
from django.conf import settings
from rest_framework import generics
from rest_framework import status as drf_status
from rest_framework.response import Response

from .models import PlayerCharacter
from .models import NonPlayerCharacter
from .serializers import character_serializer
from .serializers import PCSerializer
from .serializers import NPCSerializer


class CharacterListCreate(generics.ListCreateAPIView):

    def get_queryset(self):
        return PlayerCharacter.objects.all()

    def get_serializer_class(self):
        return PCSerializer


    def create(self, request, version, *args, **kwargs):
        character_type = request.data.pop('type')
        try:
            character = globals()[character_type].create(**request.data)
            character.save()
        except IntegrityError:
            return Response('Error try to create character', status=drf_status.HTTP_409_CONFLICT)

        return Response('Character created', status=drf_status.HTTP_201_CREATED)

    def list(self, request, version, *args, **kwargs):
        npc = NonPlayerCharacter.objects.filter(**request.data)
        pc = NonPlayerCharacter.objects.filter(**request.data)
        characters = PCSerializer(pc, many=True).data + NPCSerializer(npc, many=True).data
        return Response(characters)


class CharacterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerCharacter.objects.all()
    serializer_class = PCSerializer


    def destroy(self, request, version, pk, *args, **kwargs):
        character_type = request.data.get('type', None)
        try:
            character = globals()[character_type].objects.get(pk=pk)
            character.delete()
        except:
            return Response(status=drf_status.HTTP_400_BAD_REQUEST)
        return Response(status=drf_status.HTTP_204_NO_CONTENT)


    def update(self, request, version, pk, *args, **kwargs):
        return Response()

    def retrieve(self, request, version, pk, *args, **kwargs):
        character_type = request.query_params.get('type', None)
        if not character_type:
            return Response(status=drf_status.HTTP_400_BAD_REQUEST)

        try:
            character = globals()[character_type].objects.get(pk=pk)
        except:
            return Response(status=drf_status.HTTP_400_BAD_REQUEST)
        return Response(character_serializer(character))

