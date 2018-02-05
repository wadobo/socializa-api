from django.contrib.auth.models import User
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory import (
    Faker,
    LazyAttribute,
    LazyFunction,
    SubFactory
)
from faker import Faker as faker_Faker

from .models import Game
from .models import Preference


class PreferenceFactory(DjangoModelFactory):
    class Meta:
        model = Preference


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game

    preferences = SubFactory(PreferenceFactory)
