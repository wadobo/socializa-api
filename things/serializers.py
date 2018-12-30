from rest_framework import serializers

from .models import Item, Knowledge, Rol


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class KnowledgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Knowledge
        fields = '__all__'


class RolSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rol
        fields = '__all__'
