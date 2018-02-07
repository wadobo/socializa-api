from rest_framework import serializers


class PreferenceSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    vision_distance = serializers.IntegerField(min_value=1)
    meeting_distance = serializers.IntegerField(min_value=1)
    visible_character = serializers.BooleanField(default=True)


class GameSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    is_template = serializers.BooleanField(default=True)
    preferences = PreferenceSerializer()
