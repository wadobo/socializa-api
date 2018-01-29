from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APITestCase

from base.client import BaseClient
from .factories import NPCFactory, PlayerFactory
from .models import NPC, Player
from .serializers import NPCSerializer, PlayerSerializer


class CharacterTestCase(APITestCase):

    def setUp(self):
        User.objects.create_superuser(username='me@socializa.com',
                                      password='qweqweqwe',
                                      email='me@socializa.com')
        call_command('socialapps')
        self.client = BaseClient(version=settings.VERSION)
        self.player = PlayerFactory.create()
        self.npc = NPCFactory.create()

    def tearDown(self):
        self.client = None

    def authenticate(self, username='me@socializa.com', pwd='qweqweqwe'):
        response = self.client.authenticate(username, pwd)
        self.assertEqual(response.status_code, 200)

    def test_character_login(self):
        self.authenticate()

    def character_register(self, character_type):
        self.assertEqual(globals()[character_type].objects.count(), 1)
        data = {
            'email': 'test@socializa.com',
            'password': 'qweqweqwe',
            'type': character_type
        }
        response = self.client.post('/character/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(globals()[character_type].objects.count(), 2)
        response = self.client.post('/character/', data)
        self.assertEqual(response.status_code, 409)

    def test_player_register(self):
        self.character_register('Player')

    def test_npc_register(self):
        self.character_register('NPC')

    def test_character_list(self):
        response = self.client.get('/character/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)  # player + npc
        self.assertEqual(response.json(), [PlayerSerializer(self.player).data, NPCSerializer(self.npc).data])

    def character_update(self, character, serializer):
        character_type = character.__class__.__name__
        data = {
            'type': character_type
        }
        response = self.client.patch('/character/{0}/'.format(character.pk), data)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.json(), serializer(character, many=False).data)

    def character_retrieve(self, character, serializer):
        character_type = character.__class__.__name__
        response = self.client.get('/character/{0}/?type={1}'.format(character.pk, character_type))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), serializer(character, many=False).data)

    def character_destroy(self, character_type, pk):
        self.assertEqual(globals()[character_type].objects.count(), 1)
        data = {'type': character_type}
        response = self.client.delete('/character/{0}/'.format(pk), data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(globals()[character_type].objects.count(), 0)

    def test_player_retrieve(self):
        self.character_retrieve(self.player, PlayerSerializer)

    def test_npc_retrieve(self):
        self.character_retrieve(self.npc, NPCSerializer)

    def test_player_destroy(self):
        self.character_destroy('Player', self.player.pk)

    def test_npc_destroy(self):
        self.character_destroy('NPC', self.npc.pk)
