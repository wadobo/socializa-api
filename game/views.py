from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_200_OK as ST_200,
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_401_UNAUTHORIZED as ST_401,
)

from .models import Game
from .serializers import GameSerializer
from contents.serializers import ContentSerializer
from owner.models import Owner


class GameListCreate(generics.ListCreateAPIView):
    serializer_class = GameSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            games = Game.objects.all()
        else:
            player = self.request.user.character_player
            games = Game.objects.filter(owners__in=player.owners.all())
        try:
            games = games.filter(**self.request.query_params.dict())
        except (ValueError, FieldError):
            games = []
        return games

    def create(self, request, version, *args, **kwargs):
        contents = request.data.pop('contents', [])
        response = super().create(request, version, *args, **kwargs)
        if response.status_code == 201:
            game_id = response.data.get('id')
            owner = Owner(player=request.user.character_player, game_id=game_id)
            owner.save()
            objs = []
            for content in contents:
                content.update({'game': game_id})
                ser = ContentSerializer(data=content)
                if ser.is_valid():
                    objs.append(ser.save())
                else:
                    print(ser.errors)
                    # REMOVE bad creations
                    delete = [obj.delete() for obj in objs]
                    owner.game.delete()
                    owner.delete()
                    ser.is_valid(raise_exception=True)
        return response


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            games = Game.objects.all()
        else:
            player = self.request.user.character_player
            games = Game.objects.filter(owners__in=player.owners.all())
        return games
