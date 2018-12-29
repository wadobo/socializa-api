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
        call_command('socialapps')
        self.client = BaseClient()
        self.player = PlayerFactory.create()
        self.item = ItemFactory.create()

    def tearDown(self):
        self.client = None

    def authenticate(self, pwd='qweqweqwe'):
        self.client.authenticate(self.player.user.username, pwd)

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
        self.authenticate()
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
        self.authenticate()
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
        self.authenticate()
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
        call_command('socialapps')
        self.client = BaseClient()
        self.player = PlayerFactory.create()
        self.kn = KnowledgeFactory.create()

    def tearDown(self):
        self.client = None

    def authenticate(self, pwd='qweqweqwe'):
        self.client.authenticate(self.player.user.username, pwd)

    def test_knowledge_create(self):
        knowledges_quantity = Knowledge.objects.count()
        data = {
            'name': 'Knowledge',
            'description': 'Knowledge description',
            'shareable': True,
        }

        response = self.client.post('/thing/knowledge/', data)
        self.assertEqual(response.status_code, 401)
        self.authenticate()
        response = self.client.post('/thing/knowledge/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Knowledge.objects.count(), knowledges_quantity + 1)

    def test_knowledge_list(self, ):
        response = self.client.get('/thing/knowledge/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json(), [KnowledgeSerializer(self.kn).data])

    def test_knowledge_retrieve(self):
        response = self.client.get('/thing/knowledge/{}/'.format(self.kn.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), KnowledgeSerializer(self.kn).data)

    def test_knowledge_retrieve_unknow(self):
        response = self.client.get('/thing/knowledge/-1/')
        self.assertEqual(response.status_code, 404)

    def test_knowledge_destroy_unauthorized(self):
        response = self.client.delete('/thing/knowledge/{}/'.format(self.kn.pk))
        self.assertEqual(response.status_code, 401)

    def test_knowledge_destroy(self):
        self.authenticate()
        response = self.client.delete('/thing/knowledge/{}/'.format(self.kn.pk))
        self.assertEqual(response.status_code, 204)

    def test_knowledge_update_unauthorized(self):
        data = {
            'name': 'Knowledge',
            'description': 'Knowledge description',
            'shareable': True,
        }
        response = self.client.put('/thing/knowledge/{}/'.format(self.kn.pk), data)
        self.assertEqual(response.status_code, 401)

    def test_knowledge_update(self):
        self.authenticate()
        data = {
            'name': 'Knowledge',
            'description': 'Knowledge description',
            'shareable': True,
        }
        response = self.client.put('/thing/knowledge/{}/'.format(self.kn.pk), data)
        self.assertEqual(response.status_code, 200)
        knowledge_changed = Knowledge.objects.get(pk=self.kn.pk)
        for key, value in data.items():
            field = getattr(knowledge_changed, key)
            self.assertEqual(field, value)


class RolTestCase(APITestCase):

    def setUp(self):
        call_command('socialapps')
        self.client = BaseClient()
        self.player = PlayerFactory.create()
        self.rol = RolFactory.create()

    def tearDown(self):
        self.client = None

    def authenticate(self, pwd='qweqweqwe'):
        self.client.authenticate(self.player.user.username, pwd)

    def test_rol_create(self):
        rols_quantity = Rol.objects.count()
        data = {
            'name': 'Rol',
            'description': 'Rol description',
        }

        response = self.client.post('/thing/rol/', data)
        self.assertEqual(response.status_code, 401)
        self.authenticate()
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
        self.authenticate()
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
        self.authenticate()
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
