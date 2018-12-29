from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import GEOSGeometry
from factory.django import DjangoModelFactory
from factory import (
        Faker,
        LazyAttribute,
        LazyFunction,
        SelfAttribute,
        SubFactory
)

from .models import Content
from character.factories import NPCFactory, PlayerFactory
from things.factories import ItemFactory, KnowledgeFactory, RolFactory


def gen_latlng():
    lat, lng = Faker('latlng').generate({})
    return GEOSGeometry('POINT({0} {1})'.format(lat, lng))


class ContentFactory(DjangoModelFactory):
    content_id = SelfAttribute('content.pk')
    content_type = LazyAttribute(
            lambda o: ContentType.objects.get_for_model(o.content))
    position = LazyFunction(gen_latlng)

    class Meta:
        exclude = ['content']
        abstract = True


class ContentPlayerFactory(ContentFactory):
    content = SubFactory(PlayerFactory)

    class Meta:
        model = Content


class ContentNPCFactory(ContentFactory):
    content = SubFactory(NPCFactory)

    class Meta:
        model = Content


class ContentItemFactory(ContentFactory):
    content = SubFactory(ItemFactory)

    class Meta:
        model = Content


class ContentKnowledgeFactory(ContentFactory):
    content = SubFactory(KnowledgeFactory)

    class Meta:
        model = Content


class ContentRolFactory(ContentFactory):
    content = SubFactory(RolFactory)

    class Meta:
        model = Content
