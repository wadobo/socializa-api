from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory import (
    Faker,
    LazyAttribute,
    LazyFunction,
    PostGenerationMethodCall,
    SubFactory
)
from faker import Faker as faker_Faker

from .models import NPC
from .models import Player


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('email')
    password = PostGenerationMethodCall('set_password', 'qweqweqwe')
    email = LazyAttribute(lambda u: u.username)
    date_joined = LazyFunction(timezone.now)


def new_position(self):
    fake = faker_Faker()
    return GEOSGeometry('POINT({0} {1})'.format(fake.latitude(), fake.longitude()))


class CharacterFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    #position = LazyAttribute(new_position)

    class Meta:
        abstract = True


class NPCFactory(CharacterFactory):
    class Meta:
        model = NPC


class PlayerFactory(CharacterFactory):
    class Meta:
        model = Player
