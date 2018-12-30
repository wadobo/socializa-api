from django.contrib.auth.models import User
from rest_framework import serializers

from .models import NPC, Player


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class CharacterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        abstract = True


class PlayerSerializer(CharacterSerializer):

    class Meta:
        model = Player
        fields = '__all__'


class NPCSerializer(CharacterSerializer):

    def is_valid(self, raise_exception=True):
        email = self.initial_data.get('user', {}).get('email')
        username = self.initial_data.get('user', {}).get('username')
        if email and not username:
            self.initial_data['user']['username'] = email.split('@')[0]
        return super().is_valid(raise_exception=raise_exception)

    def create(self, data):
        user_ser = UserSerializer(data=data.pop('user'))
        user_ser.is_valid(raise_exception=True)
        data['user'] = user_ser.save()
        return super().create(data)

    def update(self, instance, data):
        user_ser = UserSerializer(instance.user, data=data.pop('user'))
        user_ser.is_valid(raise_exception=True)
        data['user'] = user_ser.save()
        return super().update(instance, data)

    class Meta:
        model = NPC
        fields = '__all__'
