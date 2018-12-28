from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APITestCase
from urllib.parse import urlencode

from base.client import BaseClient
from .factories import NPCFactory
from .models import NPC
from .serializers import NPCSerializer


class NPCTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='me@socializa.com',
              password='qweqweqwe', email='me@socializa.com')
        call_command('socialapps')
        self.client = BaseClient(version=settings.VERSION)
        self.npc = NPCFactory.create()
        self.data = {
            'user': {
                'email': 'test@test.com',
                'password': 'qwerty'
            }
        }

    def tearDown(self):
        self.client = None

    def authenticate(self, username='me@socializa.com', pwd='qweqweqwe'):
        response = self.client.authenticate(username, pwd)
        self.assertEqual(response.status_code, 200)

    # CREATE
    def character_create(self, ctype, data, st):
        self.data.update(data)
        response = self.client.post('/character/{}/'.format(ctype), self.data)
        self.assertEqual(response.status_code, st)
        return response

    def test_npc_create_unauth(self):
        self.character_create('npc', {}, 401)

    def test_npc_create_bad_request(self):
        self.authenticate()
        self.character_create('npc', {'user': {'password': 'qwerty'}}, 400)
        data = {'user': {
            'email': 'a',
            'password': 'qwerty'
        }}
        self.character_create('npc', data, 400)

    def test_npc_create_exist(self):
        self.authenticate()
        data = {'user': {
            'email': self.user.email,
            'password': 'qweqweqwe'
        }}
        self.character_create('npc', data, 400)

    def test_npc_create(self):
        initial_npc = NPC.objects.count()
        initial_user = User.objects.count()
        self.authenticate()
        response = self.character_create('npc', {}, 201)
        self.assertEqual(initial_npc + 1, NPC.objects.count())
        self.assertEqual(initial_user + 1, User.objects.count())
        self.assertFalse('password' in response.json().get('user'))

    # LIST
    def character_list(self, ctype, st, params):
        filters = '?{}'.format(urlencode(params)) if params else ''
        response = self.client.get('/character/{0}/{1}'.format(ctype, filters))
        self.assertEqual(response.status_code, st)
        return response

    def test_npc_list_filter(self):
        NPCFactory.create_batch(10)
        params = {'search': 'gmail'}
        response = self.character_list('npc', 200, params)
        query = {'user__username__icontains': params.get('search')}
        self.assertEqual(len(response.json()),
                NPC.objects.filter(**query).count())

    def test_npc_list(self):
        response = self.character_list('npc', 200, None)
        self.assertEqual(len(response.json()), 1)

    # DESTROY
    def character_destroy(self, ctype, st, pk):
        response = self.client.delete('/character/{0}/{1}/'.format(ctype, pk))
        self.assertEqual(response.status_code, st)
        return response

    def test_npc_destroy_unauth(self):
        self.character_destroy('npc', 401, self.npc.pk)

    def test_npc_destroy_bad_request(self):
        self.authenticate()
        self.character_destroy('npc', 404, self.npc.pk + 1)

    def test_npc_destroy(self):
        initial_npc = NPC.objects.count()
        initial_user = User.objects.count()
        self.authenticate()
        self.character_destroy('npc', 204, self.npc.pk)
        self.assertEqual(initial_npc - 1, NPC.objects.count())
        self.assertEqual(initial_user - 1, User.objects.count())

    # RETRIEVE
    def character_retrieve(self, ctype, st, pk):
        response = self.client.get('/character/{0}/{1}/'.format(ctype, pk))
        self.assertEqual(response.status_code, st)
        return response

    def test_npc_retrieve_bad_request(self):
        self.character_retrieve('npc', 404, self.npc.pk + 1)

    def test_npc_retrieve(self):
        self.authenticate()
        response = self.character_retrieve('npc', 200, self.npc.pk)
        self.assertEqual(response.json(), NPCSerializer(self.npc).data)

    # UPDATE
    def character_update(self, ctype, data, st, pk):
        self.data.update(data)
        response = self.client.put('/character/{0}/{1}/'.format(ctype, pk),
                self.data)
        self.assertEqual(response.status_code, st)
        return response

    def test_npc_update_unauth(self):
        self.character_update('npc', {}, 401, self.npc.pk)

    def test_npc_update_bad_request(self):
        self.authenticate()
        self.character_update('npc', {}, 404, self.npc.pk + 1)
        data = {
            'user': {
                'bad': 'bad'
            }
        }
        self.character_update('npc', data, 400, self.npc.pk)

    def test_npc_update(self):
        self.authenticate()
        data = {
            'user': {
                'username': 'other'
            }
        }
        response = self.character_update('npc', data, 200, self.npc.pk)
        self.assertEqual(response.json()['user']['username'],
                data['user']['username'])
