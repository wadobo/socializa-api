from django.conf import settings
from rest_framework.test import APITestCase

from base.client import BaseClient
from .factories import NPCFactory, PCFactory, UserFactory
from .models import Character
from .models import NonPlayerCharacter
from .models import PlayerCharacter
from .serializers import PCSerializer
from .serializers import NPCSerializer


class CharacterTestCase(APITestCase):

    fixtures = ['applications.json']

    def setUp(self):
        self.client = BaseClient(version=settings.VERSION)  # Check last version
        self.pc = PCFactory.create()
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

    def test_pc_register(self):
        self.character_register('PlayerCharacter')

    def test_npc_register(self):
        self.character_register('NonPlayerCharacter')

    def test_character_list(self):
        response = self.client.get('/character/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)  # npc + pc
        self.assertEqual(response.json()[0], PCSerializer(self.pc).data)

    def character_update(self, character_type, pk):
        data = {
            'type': character_type,
            'position': None
        }
        response = self.client.patch('/character/{0}/'.format(pk), data)
        self.assertEqual(response.status_code, 200)

    def character_retrieve(self, character, serializer):
        character_type = character.__class__.__name__
        response = self.client.get('/character/{0}/?type={1}'.format(character.pk, character_type))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), serializer(character, many=False).data)

    def character_destroy(self, character_type, pk):
        data = {'type': character_type}
        response = self.client.delete('/character/{0}/'.format(pk), data)
        self.assertEqual(response.status_code, 204)

    def test_pc_retrieve(self):
        self.character_retrieve(self.pc, PCSerializer)

    def test_npc_retrieve(self):
        self.character_retrieve(self.npc, NPCSerializer)

    def test_pc_update(self):
        self.character_update('PlayerCharacter', self.pc.pk)

    def test_npc_update(self):
        self.character_update('NonPlayerCharacter', self.npc.pk)

    def test_pc_destroy(self):
        self.character_destroy('PlayerCharacter', self.pc.pk)

    def test_npc_destroy(self):
        self.character_destroy('NonPlayerCharacter', self.npc.pk)
