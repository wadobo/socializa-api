from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_200_OK as ST_200,
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_401_UNAUTHORIZED as ST_401,
)

from owner.models import Owner
from .models import Game
from .serializers import GameSerializer


class GameListCreate(generics.ListCreateAPIView):

    def create(self, request, version, *args, **kwargs):
        # TODO: authentication
        if request.user.is_anonymous:
            return Response('', status=ST_401)
        ser = GameSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        game = ser.save()
        owner = Owner(player=request.user.character_player, game=game)
        owner.save()
        return Response('Game created', status=ST_201)

    def list(self, request, version, *args, **kwargs):
        games = Game.objects.filter(**request.data)
        games = GameSerializer(games, many=True).data
        return Response(games)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        player = self.request.user.character_player
        return Game.objects.filter(owners__in=player.owners.all())

    def destroy(self, request, version, pk, *args, **kwargs):
        if request.user.is_anonymous:
            return Response('', status=ST_401)
        self.get_object().delete()
        return Response(status=ST_204)

    def update(self, request, version, pk, *args, **kwargs):
        if request.user.is_anonymous:
            return Response('', status=ST_401)
        ser = GameSerializer(self.get_object(), data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response('Game updated', status=ST_200)

    def retrieve(self, request, version, pk, *args, **kwargs):
        game = get_object_or_404(Game, pk=pk)
        return Response(GameSerializer(game).data)
