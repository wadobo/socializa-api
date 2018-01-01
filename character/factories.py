from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory import (
    Faker,
    LazyAttribute,
    LazyFunction,
    SubFactory
)
from faker import Faker as faker_Faker

from .models import NonPlayerCharacter
from .models import PlayerCharacter


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('email')
    email = LazyAttribute(lambda u: u.username)
    date_joined = LazyFunction(timezone.now)


def new_position(self):
    fake = faker_Faker()
    return GEOSGeometry('POINT({0} {1})'.format(fake.latitude(), fake.longitude()))


class NPCFactory(DjangoModelFactory):
    class Meta:
        model = NonPlayerCharacter

    user = SubFactory(UserFactory)
    position = LazyAttribute(new_position)


class PCFactory(DjangoModelFactory):
    class Meta:
        model = PlayerCharacter

    user = SubFactory(UserFactory)
    position = LazyAttribute(new_position)
