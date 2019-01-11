from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.measure import D
from django.core.exceptions import FieldError
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from character.models import Player
from contents.models import Content
from contents.serializers import ContentSerializer
from owner.models import Owner
from .models import Game
from .serializers import GameSerializer


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
        response = super().create(request, version, *args, **kwargs)
        if response.status_code == 201:
            game_id = response.data.get('id')
            owner = Owner(player=request.user.character_player, game_id=game_id)
            owner.save()
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


class GameStatusForPlayer(views.APIView):
    """
    This call return everycontents of game that is near player.
    Call format: GET /api/{version}/game/{game_pk}/status/
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, version, pk, *args, **kwargs):
        self.player = Player.objects.get(user=request.user)
        player_ctype = ContentType.objects.get(model='player')
        self.player_content = get_object_or_404(
            Content, content_type=player_ctype, content_id=self.player.pk)
        game = get_object_or_404(Game, pk=pk)
        contents = Content.objects.filter(game=game)

        q = Q(position__distance_lte=(self.player_content.position,
                                      D(m=game.preferences.vision_distance)))

        result = {
            'npcs': [ContentSerializer(x).data
                     for x in contents.filter(content_type=ContentType.objects.get(model='npc'))
                                      .filter(q)],
            'players': [ContentSerializer(x).data
                        for x in contents.filter(content_type=ContentType.objects.get(model='player'))
                                         .filter(q)
                                         .exclude(pk=self.player_content.pk)],
            'items': [ContentSerializer(x).data
                      for x in contents.filter(content_type=ContentType.objects.get(model='item'))
                                       .filter(q)]
        }

        return Response(result)


class PlayerJoinToGame(views.APIView):
    """
    This call should add Player to Content in a give position.
    Player will be the player that realize call.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        game = get_object_or_404(Game, pk=kwargs['pk'])
        position = self.request.data.get("position", None)
        player = Player.objects.get(user=self.request.user)
        content_type = ContentType.objects.get(model='player')
        data = {
            'game': game.pk,
            'content_type': content_type.pk,
            'content_id': player.pk,
            'position': position
        }
        instance = Content.objects.filter(game=game, content_id=player.pk,
                                         content_type=content_type)
        if instance.exists():
            content_ser = ContentSerializer(instance.first(), data=data)
            st = status.HTTP_200_OK
        else:
            content_ser = ContentSerializer(data=data)
            st = status.HTTP_201_CREATED
        content_ser.is_valid(raise_exception=True)
        content = content_ser.save()
        return Response({}, st)
