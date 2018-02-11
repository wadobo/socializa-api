from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APITestCase

from base.client import BaseClient
from character.factories import PlayerFactory
from .factories import ItemFactory
from .factories import KnowledgeFactory
from .factories import RolFactory
from .models import Item
from .models import Knowledge
from .models import Rol
from .serializers import ItemSerializer
from .serializers import KnowledgeSerializer
from .serializers import RolSerializer


class ItemTestCase(APITestCase):

    def setUp(self):
        User.objects.create_superuser(username='me@socializa.com',
                                      password='qweqweqwe',
                                      email='me@socializa.com')
        call_command('socialapps')
        self.client = BaseClient(version=settings.VERSION)
        self.player = PlayerFactory.create()
        self.item = ItemFactory.create()

    def tearDown(self):
        self.client = None

    def authenticate(self, username='me@socializa.com', pwd='qweqweqwe'):
        response = self.client.authenticate(username, pwd)
        self.assertEqual(response.status_code, 200)

    def test_item_create(self):
        items_quantity = Item.objects.count()
        data = {
            'name': 'Item',
            'description': 'Item description',
            'shareable': True,
            'pickable': True,
            'consumable': True,
        }

        response = self.client.post('/thing/item/', data)
        self.assertEqual(response.status_code, 401)
        self.authenticate(username=self.player.user.username)
        response = self.client.post('/thing/item/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Item.objects.count(), items_quantity + 1)

    def test_item_list(self, ):
        response = self.client.get('/thing/item/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json(), [ItemSerializer(self.item).data])

    def test_item_retrieve(self):
        response = self.client.get('/thing/item/{}/'.format(self.item.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ItemSerializer(self.item).data)

    def test_item_retrieve_unknow(self):
        response = self.client.get('/thing/item/-1/')
        self.assertEqual(response.status_code, 404)

    def test_item_destroy_unauthorized(self):
        response = self.client.delete('/thing/item/{}/'.format(self.item.pk))
        self.assertEqual(response.status_code, 401)

    def test_item_destroy(self):
        self.authenticate(username=self.player.user.username)
        response = self.client.delete('/thing/item/{}/'.format(self.item.pk))
        self.assertEqual(response.status_code, 204)

    def test_item_update_unauthorized(self):
        data = {
            'name': 'Item',
            'description': 'Item description',
            'shareable': True,
            'pickable': True,
            'consumable': True,
        }
        response = self.client.put('/thing/item/{}/'.format(self.item.pk), data)
        self.assertEqual(response.status_code, 401)

    def test_item_update(self):
        self.authenticate(username=self.player.user.username)
        data = {
            'name': 'Item',
            'description': 'Item description',
            'shareable': True,
            'pickable': True,
            'consumable': True,
        }
        response = self.client.put('/thing/item/{}/'.format(self.item.pk), data)
        self.assertEqual(response.status_code, 200)
        item_changed = Item.objects.get(pk=self.item.pk)
        for key, value in data.items():
            field = getattr(item_changed, key)
            self.assertEqual(field, value)


class KnowledgeTestCase(APITestCase):

    def setUp(self):
        User.objects.create_superuser(username='me@socializa.com',
                                      password='qweqweqwe',
                                      email='me@socializa.com')
        call_command('socialapps')
        self.client = BaseClient(version=settings.VERSION)
        self.player = PlayerFactory.create()
        self.knowledge = KnowledgeFactory.create()

    def tearDown(self):
        self.client = None

    def authenticate(self, username='me@socializa.com', pwd='qweqweqwe'):
        response = self.client.authenticate(username, pwd)
        self.assertEqual(response.status_code, 200)

    def test_knowledge_create(self):
        knowledges_quantity = Knowledge.objects.count()
        data = {
            'name': 'Knowledge',
            'description': 'Knowledge description',
            'shareable': True,
        }

        response = self.client.post('/thing/knowledge/', data)
        self.assertEqual(response.status_code, 401)
        self.authenticate(username=self.player.user.username)
        response = self.client.post('/thing/knowledge/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Knowledge.objects.count(), knowledges_quantity + 1)

    def test_knowledge_list(self, ):
        response = self.client.get('/thing/knowledge/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json(), [KnowledgeSerializer(self.knowledge).data])

    def test_knowledge_retrieve(self):
        response = self.client.get('/thing/knowledge/{}/'.format(self.knowledge.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), KnowledgeSerializer(self.knowledge).data)

    def test_knowledge_retrieve_unknow(self):
        response = self.client.get('/thing/knowledge/-1/')
        self.assertEqual(response.status_code, 404)

    def test_knowledge_destroy_unauthorized(self):
        response = self.client.delete('/thing/knowledge/{}/'.format(self.knowledge.pk))
        self.assertEqual(response.status_code, 401)

    def test_knowledge_destroy(self):
        self.authenticate(username=self.player.user.username)
        response = self.client.delete('/thing/knowledge/{}/'.format(self.knowledge.pk))
        self.assertEqual(response.status_code, 204)

    def test_knowledge_update_unauthorized(self):
        data = {
            'name': 'Knowledge',
            'description': 'Knowledge description',
            'shareable': True,
        }
        response = self.client.put('/thing/knowledge/{}/'.format(self.knowledge.pk), data)
        self.assertEqual(response.status_code, 401)

    def test_knowledge_update(self):
        self.authenticate(username=self.player.user.username)
        data = {
            'name': 'Knowledge',
            'description': 'Knowledge description',
            'shareable': True,
        }
        response = self.client.put('/thing/knowledge/{}/'.format(self.knowledge.pk), data)
        self.assertEqual(response.status_code, 200)
        knowledge_changed = Knowledge.objects.get(pk=self.knowledge.pk)
        for key, value in data.items():
            field = getattr(knowledge_changed, key)
            self.assertEqual(field, value)


class RolTestCase(APITestCase):

    def setUp(self):
        User.objects.create_superuser(username='me@socializa.com',
                                      password='qweqweqwe',
                                      email='me@socializa.com')
        call_command('socialapps')
        self.client = BaseClient(version=settings.VERSION)
        self.player = PlayerFactory.create()
        self.rol = RolFactory.create()

    def tearDown(self):
        self.client = None

    def authenticate(self, username='me@socializa.com', pwd='qweqweqwe'):
        response = self.client.authenticate(username, pwd)
        self.assertEqual(response.status_code, 200)

    def test_rol_create(self):
        rols_quantity = Rol.objects.count()
        data = {
            'name': 'Rol',
            'description': 'Rol description',
        }

        response = self.client.post('/thing/rol/', data)
        self.assertEqual(response.status_code, 401)
        self.authenticate(username=self.player.user.username)
        response = self.client.post('/thing/rol/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Rol.objects.count(), rols_quantity + 1)

    def test_rol_list(self, ):
        response = self.client.get('/thing/rol/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json(), [RolSerializer(self.rol).data])

    def test_rol_retrieve(self):
        response = self.client.get('/thing/rol/{}/'.format(self.rol.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), RolSerializer(self.rol).data)

    def test_rol_retrieve_unknow(self):
        response = self.client.get('/thing/rol/-1/')
        self.assertEqual(response.status_code, 404)

    def test_rol_destroy_unauthorized(self):
        response = self.client.delete('/thing/rol/{}/'.format(self.rol.pk))
        self.assertEqual(response.status_code, 401)

    def test_rol_destroy(self):
        self.authenticate(username=self.player.user.username)
        response = self.client.delete('/thing/rol/{}/'.format(self.rol.pk))
        self.assertEqual(response.status_code, 204)

    def test_rol_update_unauthorized(self):
        data = {
            'name': 'Rol',
            'description': 'Rol description',
        }
        response = self.client.put('/thing/rol/{}/'.format(self.rol.pk), data)
        self.assertEqual(response.status_code, 401)

    def test_rol_update(self):
        self.authenticate(username=self.player.user.username)
        data = {
            'name': 'Rol',
            'description': 'Rol description',
        }
        response = self.client.put('/thing/rol/{}/'.format(self.rol.pk), data)
        self.assertEqual(response.status_code, 200)
        rol_changed = Rol.objects.get(pk=self.rol.pk)
        for key, value in data.items():
            field = getattr(rol_changed, key)
            self.assertEqual(field, value)
