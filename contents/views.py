from django.core.exceptions import FieldError
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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


class ContentTypes(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, version, *args, **kwargs):
        content_types_list = ('player', 'npc', 'knowledge', 'item', 'rol')
        content_types = ContentType.objects.filter(model__in=content_types_list)
        result =  {c.pk: c.model for c in content_types}
        return Response(result)