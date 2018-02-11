from rest_framework import serializers

from .models import Item
from .models import Knowledge
from .models import Rol


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('name', 'description', 'pickable', 'shareable', 'consumable')


class KnowledgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Knowledge
        fields = ('name', 'description', 'shareable')


class RolSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rol
        fields = ('name', 'description')
