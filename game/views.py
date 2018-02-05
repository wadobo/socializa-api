from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_200_OK as ST_200,
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_403_FORBIDDEN as ST_403,
        HTTP_409_CONFLICT as ST_409
)

from owner.models import Owner
from .models import Game, Preference
from .serializers import GameSerializer


class GameListCreate(generics.ListCreateAPIView):

    def create(self, request, version, *args, **kwargs):
        # TODO: authentication
        if request.user.is_anonymous:
            return Response('', status=ST_401)
        player = request.user.character_player
        try:
            preferences = Preference(**request.data.pop('preferences'))
            preferences.save()
        except IntegrityError:
            return Response('Error try to create game', status=ST_409)
        try:
            game = Game(**request.data)
            game.preferences = preferences
            game.save()
        except IntegrityError:
            return Response('Error try to create game', status=ST_409)

        owner = Owner(player=player, game=game)
        owner.save()
        return Response('Game created', status=ST_201)

    def list(self, request, version, *args, **kwargs):
        games = Game.objects.filter(**request.data)
        games = GameSerializer(games, many=True).data
        return Response(games)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):

    def destroy(self, request, version, pk, *args, **kwargs):
        if request.user.is_anonymous:
            return Response('', status=ST_401)
        game = get_object_or_404(Game, pk=pk)
        owner = get_object_or_404(Owner, player=request.user.character_player, game=game)
        game.delete()
        return Response(status=ST_204)


    def update(self, request, version, pk, *args, **kwargs):
        if request.user.is_anonymous:
            return Response('', status=ST_401)
        game = get_object_or_404(Game, pk=pk)
        owner = get_object_or_404(Owner, player=request.user.character_player, game=game)
        for field, value in request.data.pop('preferences').items():
            setattr(game.preferences, field, value)
        for field, value in request.data.items():
            setattr(game, field, value)
        game.preferences.save()
        game.save()
        return Response('Game updated', status=ST_200)


    def retrieve(self, request, version, pk, *args, **kwargs):
        game = get_object_or_404(Game, pk=pk)
        return Response(GameSerializer(game).data)


