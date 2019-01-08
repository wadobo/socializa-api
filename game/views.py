from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.measure import D
from django.core.exceptions import FieldError
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response


from owner.models import Owner
from .models import Game
from .serializers import GameSerializer
from character.models import Player
from contents.serializers import ContentSerializer
from contents.models import Content
from django.contrib.contenttypes.models import ContentType


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
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, version, pk, *args, **kwargs):
        self.player = Player.objects.get(user=request.user)
        self.player_content = Content.objects.get(content_type=ContentType.objects.get(pk=17),
                                                     content_id=self.player.pk)
        game = Game.objects.get(pk=pk)
        contents = Content.objects.filter(game=game)

        q = Q(position__distance_lte=(self.player_content.position, D(m=game.preferences.vision_distance)))

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