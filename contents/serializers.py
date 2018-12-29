from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from .models import Content
from character.models import NPC, Player
from character.serializers import NPCSerializer, PlayerSerializer
from things.models import Item, Knowledge, Rol
from things.serializers import ItemSerializer, KnowledgeSerializer, RolSerializer


SERIALIZERS = [NPCSerializer, PlayerSerializer, ItemSerializer,
        KnowledgeSerializer, RolSerializer]

def get_serializer(model):
    for ser in SERIALIZERS:
        if ser.Meta.model == model:
            return ser
    return None


class ContentRelatedField(serializers.RelatedField):
    queryset = Content.objects.all()

    def to_representation(self, value):
        if isinstance(value, Player):
            return PlayerSerializer(value).data
        elif isinstance(value, NPC):
            return NPCSerializer(value).data
        elif isinstance(value, Item):
            return ItemSerializer(value).data
        elif isinstance(value, Knowledge):
            return KnowledgeSerializer(value).data
        elif isinstance(value, Rol):
            return RolSerializer(value).data
        else:
            return None

    def to_internal_value(self, value):
        if isinstance(value, dict):
            return value
        else:
            return None


class ContentSerializer(serializers.ModelSerializer):
    content = ContentRelatedField(required=False)
    position = PointField(required=False)

    def create(self, data, *args, **kwargs):
        content_type = data.get('content_type')
        model = content_type.model_class()
        content = data.get('content')
        if content and data.get('content_id') <= 0:
            ser = get_serializer(model)(data=content)
            ser.is_valid(raise_exception=True)
            content_obj = ser.save()
            data['content'] = content_obj
            data['content_id'] = content_obj.pk
        else:
            content_id = data.get('content_id')
            content_obj = model.objects.get(pk=content_id)
            data['content'] = content_obj
        return super().create(data, *args, **kwargs)

    def update(self, instance, data, *args, **kwargs):
        content_type = data.get('content_type')
        model = content_type.model_class()
        content = data.get('content')
        if content and data.get('content_id') <= 0:
            ser = get_serializer(model)(instance.content, data=content)
            ser.is_valid(raise_exception=True)
            content_obj = ser.save()
            data['content'] = content_obj
            data['content_id'] = content_obj.pk
        else:
            content_id = data.get('content_id')
            content_obj = model.objects.get(pk=content_id)
            data['content'] = content_obj
        return super().create(data, *args, **kwargs)

    class Meta:
        model = Content
        fields = '__all__'
