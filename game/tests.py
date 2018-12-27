from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APITestCase

from .factories import GameFactory
from .models import Game
from .serializers import GameSerializer
from base.client import BaseClient
from character.models import Player
from character.factories import PlayerFactory
from contents.models import Content
from owner.models import Owner
from things.models import Item


class GameTestCase(APITestCase):

    def setUp(self):
        User.objects.create_superuser(username='me@socializa.com',
                                      password='qweqweqwe',
                                      email='me@socializa.com')
        call_command('socialapps')
        self.client = BaseClient(version=settings.VERSION)
        self.player = PlayerFactory.create()
        self.game = GameFactory.create()
        self.owner = Owner(player=self.player, game=self.game)
        self.owner.save()

        self.data = {
            'title': 'Example',
            'start': '2018-02-04T07:28:12.546030+00:00',
            'preferences': {
                'vision_distance': 100,
                'meeting_distance': 20,
                'visible_character': True
            },
        }

    def tearDown(self):
        self.client = None

    def authenticate(self, username='me@socializa.com', pwd='qweqweqwe'):
        response = self.client.authenticate(username, pwd)
        self.assertEqual(response.status_code, 200)

    def test_game_create_unauthorized(self):
        response = self.client.post('/game/', self.data)
        self.assertEqual(response.status_code, 401)

    def test_game_create_bad_request_1(self):
        self.data['preferences']['vision_distance'] = 'bad'
        self.authenticate(username=self.player.user.username)
        response = self.client.post('/game/', self.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('preferences' in response.json())
        self.assertTrue('vision_distance' in response.json().get('preferences'))

    def test_game_create_bad_request_2(self):
        self.data['start'] = 'bad'
        self.authenticate(username=self.player.user.username)
        response = self.client.post('/game/', self.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('start' in response.json())

    def test_game_create(self):
        games_amount = Game.objects.count()
        owners_amount = Owner.objects.count()

        self.authenticate(username=self.player.user.username)
        response = self.client.post('/game/', self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Game.objects.count(), games_amount + 1)
        self.assertEqual(Owner.objects.count(), owners_amount + 1)

    def test_game_list(self):
        response = self.client.get('/game/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json(), [GameSerializer(self.game).data])

    def test_game_retrieve(self):
        response = self.client.get('/game/{}/'.format(self.game.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), GameSerializer(self.game).data)

    def test_game_retrieve_unknow(self):
        response = self.client.get('/game/-1/')
        self.assertEqual(response.status_code, 404)

    def test_game_destroy_unauthorized(self):
        response = self.client.delete('/game/{}/'.format(self.game.pk))
        self.assertEqual(response.status_code, 401)

    def test_game_destroy(self):
        self.authenticate(username=self.player.user.username)
        response = self.client.delete('/game/{}/'.format(self.game.pk))
        self.assertEqual(response.status_code, 204)

    def test_game_update_unauthorized(self):
        self.data['preferences']['vision_distance'] = 80
        response = self.client.put('/game/{}/'.format(self.game.pk), self.data)
        self.assertEqual(response.status_code, 401)

    def test_game_update_bad_request_1(self):
        self.authenticate(username=self.player.user.username)
        self.data['preferences']['vision_distance'] = True
        response = self.client.put('/game/{}/'.format(self.game.pk), self.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('preferences' in response.json())
        self.assertTrue('vision_distance' in response.json().get('preferences'))

    def test_game_update_bad_request_2(self):
        self.authenticate(username=self.player.user.username)
        self.data['start'] = 'bad'
        response = self.client.put('/game/{}/'.format(self.game.pk), self.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('start' in response.json())

    def test_game_update(self):
        self.authenticate(username=self.player.user.username)
        self.data['preferences']['vision_distance'] = 80
        response = self.client.put('/game/{}/'.format(self.game.pk), self.data)
        self.assertEqual(response.status_code, 200)
        game_changed = Game.objects.get(pk=self.game.pk)
        for key, value in self.data.pop('preferences').items():
            self.assertEqual(getattr(game_changed.preferences, key), value)
        for key, value in self.data.items():
            field = getattr(game_changed, key)
            if key in ['start', 'end']:
                field = field.isoformat()
            self.assertEqual(field, value)


class GameContentTestCase(APITestCase):

    def setUp(self):
        User.objects.create_superuser(username='me@socializa.com',
                                      password='qweqweqwe',
                                      email='me@socializa.com')
        call_command('socialapps')
        self.client = BaseClient(version=settings.VERSION)
        self.player = PlayerFactory.create()
        self.ct_player = ContentType.objects.get(model='player').pk
        self.ct_npc = ContentType.objects.get(model='npc').pk
        self.ct_item = ContentType.objects.get(model='item').pk
        self.ct_knowledge = ContentType.objects.get(model='knowledge').pk
        self.ct_rol = ContentType.objects.get(model='rol').pk

    def tearDown(self):
        self.client = None
        User.objects.all().delete()
        Player.objects.all().delete()

    def authenticate(self, username='me@socializa.com', pwd='qweqweqwe'):
        response = self.client.authenticate(username, pwd)
        self.assertEqual(response.status_code, 200)

    def test_create_game_contents(self):
        self.authenticate(username=self.player.user.username)

        # Create game complete: contents
        ## Create item
        data = {
            'name': 'Item',
            'description': 'Item description',
            'shareable': True,
            'pickable': True,
            'consumable': True,
        }
        response = self.client.post('/thing/item/', data)
        self.assertEqual(response.status_code, 201)
        item = Item.objects.last()

        ## Create game with contents
        data = {
            'title': 'My game',
            'description': 'Example game',
            'start': timezone.now().isoformat(),
            'preferences': {
                'vision_distance': 100,
                'meeting_distance': 10,
                'visible_character': True
            },
            'contents': [
                {  # New, item
                    'content_type': self.ct_item,
                    'content_id': 0,
                    'content': {
                        'name': 'key',
                        'description': 'key number 1',
                        'pickable': True,
                        'shareable': False,
                        'consumable': False,
                    },
                    'position': {
                        'longitude': 37.241421,
                        'latitude': -6.9447224
                    },
                },
                {  # New, knowledge
                    'content_type': self.ct_item,
                    'content_id': 0,
                    'content': {
                        'name': 'Confidential information',
                        'description': 'This information is private and important.',
                        'pickable': True,
                        'shareable': False,
                        'consumable': False,
                    },
                    'position': {
                        'longitude': 37.221421,
                        'latitude': -6.9447224
                    },
                },
                {  # Exist, Item
                    'content_type': ContentType.objects.get_for_model(item).pk,
                    'content_id': item.pk,
                    'position': {
                        'longitude': 37.201421,
                        'latitude': -6.9447224
                    },
                },
            ]
        }
        response = self.client.post('/game/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Content.objects.count(), 3)
