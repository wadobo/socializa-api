from factory.django import DjangoModelFactory
from factory import SubFactory

from .models import Game
from .models import Preference


class PreferenceFactory(DjangoModelFactory):
    class Meta:
        model = Preference


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game

    preferences = SubFactory(PreferenceFactory)
