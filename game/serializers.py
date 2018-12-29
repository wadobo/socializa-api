from rest_framework import serializers

from .models import Game, Preference
from contents.serializers import ContentSerializer


class PreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    preferences = PreferenceSerializer()
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = '__all__'

    def create(self, data):
        p_serializer = PreferenceSerializer(data=data.pop('preferences'))
        p_serializer.is_valid(raise_exception=True)
        preferences = p_serializer.save()
        data['preferences'] = preferences
        return super().create(data)

    def update(self, instance, data):
        p_serializer = PreferenceSerializer(instance.preferences,
                data=data.pop('preferences', {}), partial=True)
        p_serializer.is_valid(raise_exception=True)
        preferences = p_serializer.save()
        data['preferences'] = preferences
        return super().update(instance, data)
