from django.contrib.auth.models import User
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory import (
    Faker,
    LazyAttribute,
    LazyFunction,
    PostGenerationMethodCall,
    SubFactory
)

from .models import NPC
from .models import Player


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('email')
    password = PostGenerationMethodCall('set_password', 'qweqweqwe')
    email = LazyAttribute(lambda u: u.username)
    date_joined = LazyFunction(timezone.now)


class CharacterFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)

    class Meta:
        abstract = True


class NPCFactory(CharacterFactory):
    class Meta:
        model = NPC


class PlayerFactory(CharacterFactory):
    class Meta:
        model = Player
