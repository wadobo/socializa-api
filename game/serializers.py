from rest_framework import serializers

from .models import Game, Preference


class PreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    preferences = PreferenceSerializer()

    class Meta:
        model = Game
        fields = '__all__'

    def create(self, data, *args, **kwargs):
        p_serializer = PreferenceSerializer(data=data.pop('preferences'))
        p_serializer.is_valid(raise_exception=True)
        preferences = p_serializer.save()
        data['preferences'] = preferences
        return super().create(data, **kwargs)

    def update(self, instance, data, *args, **kwargs):
        p_serializer = PreferenceSerializer(instance.preferences,
                data=data.pop('preferences'))
        p_serializer.is_valid(raise_exception=True)
        preferences = p_serializer.save()
        data['preferences'] = preferences
        return super().update(instance, data, **kwargs)
