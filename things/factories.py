from factory.django import DjangoModelFactory
from factory import SubFactory

from .models import Item
from .models import Knowledge
from .models import Rol


class ItemFactory(DjangoModelFactory):
    class Meta:
        model = Item


class KnowledgeFactory(DjangoModelFactory):
    class Meta:
        model = Knowledge


class RolFactory(DjangoModelFactory):
    class Meta:
        model = Rol
