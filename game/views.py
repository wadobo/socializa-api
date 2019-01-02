from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import FieldError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS

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
