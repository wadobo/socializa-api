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

from character.factories import NPCFactory
from things.factories import ItemFactory, KnowledgeFactory, RolFactory
from .models import Content


def gen_latlng():
    lat, lng = Faker('latlng').generate({})
    return GEOSGeometry('POINT({0} {1})'.format(lat, lng))


def get_content_type(data):
    return ContentType.objects.get_for_model(data.content)


class ContentFactory(DjangoModelFactory):
    content_id = SelfAttribute('content.pk')
    content_type = LazyAttribute(get_content_type)
    position = LazyFunction(gen_latlng)

    class Meta:
        exclude = ['content']
        abstract = True


class ContentPlayerFactory(ContentFactory):
    """ Need content like param because PlayerFactory not exist. """

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
