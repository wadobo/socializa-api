from django.contrib.contenttypes.models import ContentType
from factory.django import DjangoModelFactory
from factory import LazyAttribute, SelfAttribute, SubFactory

from .models import Content
from character.factories import NPCFactory, PlayerFactory
from things.factories import ItemFactory, KnowledgeFactory, RolFactory


class ContentFactory(DjangoModelFactory):
    content_id = SelfAttribute('content.pk')
    content_type = LazyAttribute(
            lambda o: ContentType.objects.get_for_model(o.content))

    class Meta:
        exclude = ['content']
        abstract = True


class ContentPlayerFactory(ContentFactory):
    content = SubFactory(PlayerFactory)

    class Meta:
        model = Content


class ContentNPCFactory(ContentFactory):
    content = SubFactory(NPCFactory)

    class Meta:
        model = Content


class ContentItemFactory(ContentFactory):
    content = SubFactory(ItemFactory)

    class Meta:
        model = Content


class ContentKnowledgeFactory(ContentFactory):
    content = SubFactory(KnowledgeFactory)

    class Meta:
        model = Content


class ContentRolFactory(ContentFactory):
    content = SubFactory(RolFactory)

    class Meta:
        model = Content
