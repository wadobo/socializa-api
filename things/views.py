from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Item, Knowledge, Rol
from .serializers import ItemSerializer, KnowledgeSerializer, RolSerializer


class ItemListCreate(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)


class KnowledgeListCreate(generics.ListCreateAPIView):
    serializer_class = KnowledgeSerializer
    queryset = Knowledge.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)


class KnowledgeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = KnowledgeSerializer
    queryset = Knowledge.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RolListCreate(generics.ListCreateAPIView):
    serializer_class = RolSerializer
    queryset = Rol.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RolDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RolSerializer
    queryset = Rol.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
