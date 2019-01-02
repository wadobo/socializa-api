from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from character.models import NPC, Player
from character.serializers import NPCSerializer, PlayerSerializer
from things.models import Item, Knowledge, Rol
from things.serializers import ItemSerializer, KnowledgeSerializer, RolSerializer
from .models import Content


SERIALIZERS = [NPCSerializer, PlayerSerializer, ItemSerializer,
               KnowledgeSerializer, RolSerializer]

def get_serializer(model):
    res = None
    for ser in SERIALIZERS:
        if ser.Meta.model == model:
            res = ser
            break
    return res


class ContentRelatedField(serializers.RelatedField):
    queryset = Content.objects.all()

    def to_representation(self, value):
        res = None
        if isinstance(value, Player):
            res = PlayerSerializer(value).data
        elif isinstance(value, NPC):
            res = NPCSerializer(value).data
        elif isinstance(value, Item):
            res = ItemSerializer(value).data
        elif isinstance(value, Knowledge):
            res = KnowledgeSerializer(value).data
        elif isinstance(value, Rol):
            res = RolSerializer(value).data
        return res

    def to_internal_value(self, value):
        return value if isinstance(value, dict) else None


class ContentSerializer(serializers.ModelSerializer):
    content = ContentRelatedField(required=False)
    position = PointField(required=False)

    def create(self, data):
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
        return super().create(data)

    def update(self, instance, data):
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
        return super().update(instance, data)

    class Meta:
        model = Content
        fields = '__all__'
