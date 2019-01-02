from django.core.exceptions import FieldError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from game.models import Game
from .models import Content
from .serializers import ContentSerializer


class ContentListCreate(generics.ListCreateAPIView):
    serializer_class = ContentSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        player = self.request.user.character_player
        games = Game.objects.filter(owners__in=player.owners.all())
        contents = Content.objects.filter(game__in=games)
        try:
            contents = contents.filter(**self.request.query_params.dict())
        except (ValueError, FieldError):
            contents = []
        return contents


class ContentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        player = self.request.user.character_player
        games = Game.objects.filter(owners__in=player.owners.all())
        return Content.objects.filter(game__in=games)
