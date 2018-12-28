from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics

from .models import NPC
from .serializers import NPCSerializer


class NPCListCreate(generics.ListCreateAPIView):
    serializer_class = NPCSerializer
    queryset = NPC.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username',)


class NPCDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NPCSerializer
    queryset = NPC.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
