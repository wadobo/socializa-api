from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APITestCase

from .factories import GameFactory
from .models import Game
from .serializers import GameSerializer
from base.client import BaseClient
from character.factories import PlayerFactory
from owner.models import Owner


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

    def tearDown(self):
        self.client = None

    def authenticate(self, username='me@socializa.com', pwd='qweqweqwe'):
        response = self.client.authenticate(username, pwd)
        self.assertEqual(response.status_code, 200)

    def test_game_create_unauthorized(self):
        data = {
            'title': 'Example',
            'start': '2018-02-04T07:28:12.546030+00:00',
            'preferences': {
                'vision_distance': 100,
                'meeting_distance': 20,
                'visible_character': True
            }
        }
        response = self.client.post('/game/', data)
        self.assertEqual(response.status_code, 401)

    def test_game_create_bad_request(self):
        data = {
            'title': 'Example',
            'start': '2018-02-04T07:28:12.546030+00:00',
            'preferences': {
                'vision_distance': 'bad',
                'meeting_distance': 20,
                'visible_character': True
            }
        }
        self.authenticate(username=self.player.user.username)
        response = self.client.post('/game/', data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('preferences' in response.json())
        self.assertTrue('vision_distance' in response.json().get('preferences'))

        data = {
            'title': 'Example',
            'start': 'bad',
            'preferences': {
                'vision_distance': 100,
                'meeting_distance': 20,
                'visible_character': True
            }
        }
        response = self.client.post('/game/', data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('start' in response.json())

    def test_game_create(self):
        games_amount = Game.objects.count()
        owners_amount = Owner.objects.count()
        data = {
            'title': 'Example',
            'start': '2018-02-04T07:28:12.546030+00:00',
            'preferences': {
                'vision_distance': 100,
                'meeting_distance': 20,
                'visible_character': True
            }
        }

        self.authenticate(username=self.player.user.username)
        response = self.client.post('/game/', data)
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
        data = {
            'title': 'Example 2',
            'start': '2018-02-04T07:28:12.546030+00:00',
            'preferences': {
                'vision_distance': 80,
                'meeting_distance': 40,
                'visible_character': True
            }
        }
        response = self.client.put('/game/{}/'.format(self.game.pk), data)
        self.assertEqual(response.status_code, 401)

    def test_game_update_bad_request(self):
        self.authenticate(username=self.player.user.username)
        data = {
            'title': 'Example 2',
            'start': '2019-02-04T07:28:12.546030+00:00',
            'preferences': {
                'vision_distance': True,
                'meeting_distance': 40,
                'visible_character': False
            }
        }
        response = self.client.put('/game/{}/'.format(self.game.pk), data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('preferences' in response.json())
        self.assertTrue('vision_distance' in response.json().get('preferences'))

        data = {
            'title': 'Example',
            'start': 'bad',
            'preferences': {
                'vision_distance': 100,
                'meeting_distance': 20,
                'visible_character': True
            }
        }
        response = self.client.put('/game/{}/'.format(self.game.pk), data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('start' in response.json())

    def test_game_update(self):
        self.authenticate(username=self.player.user.username)
        data = {
            'title': 'Example 2',
            'start': '2019-02-04T07:28:12.546030+00:00',
            'preferences': {
                'vision_distance': 80,
                'meeting_distance': 40,
                'visible_character': False
            }
        }
        response = self.client.put('/game/{}/'.format(self.game.pk), data)
        self.assertEqual(response.status_code, 200)
        game_changed = Game.objects.get(pk=self.game.pk)
        for key, value in data.pop('preferences').items():
            self.assertEqual(getattr(game_changed.preferences, key), value)
        for key, value in data.items():
            field = getattr(game_changed, key)
            if key in ['start', 'end']:
                field = field.isoformat()
            self.assertEqual(field, value)
