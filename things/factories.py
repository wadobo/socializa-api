from factory.django import DjangoModelFactory

from .models import (
    Item,
    Knowledge,
    Rol,
)


class ThingFactory(DjangoModelFactory):
    class Meta:
        abstract = True


class ItemFactory(ThingFactory):
    class Meta:
        model = Item


class KnowledgeFactory(ThingFactory):
    class Meta:
        model = Knowledge


class RolFactory(ThingFactory):
    class Meta:
        model = Rol
