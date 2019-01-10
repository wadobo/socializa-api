from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import FieldError
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from owner.models import Owner
from .models import Game
from character.models import Player
from .serializers import GameSerializer
from contents.models import Content

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

        if not position or not position['longitude'] or not position['latitude']:
            return Response({"message": "Position error"},
                            status.HTTP_400_BAD_REQUEST)

        content = Content.objects.filter(game=game,
                                         content_type=content_type,
                                         content_id=player.pk).first()
        position_point = Point(position['longitude'], position['latitude'])

        if not content:
            Content.objects.create(game=game,
                                   content_type=content_type,
                                   content_id=player.pk,
                                   position=position_point)
            return Response({}, status.HTTP_201_CREATED)
        else:
            content.position = position_point
            content.save()
            return Response({}, status.HTTP_200_OK)
