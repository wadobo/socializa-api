from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.utils import timezone

from base.tests import BaseTestCase
from contents.factories import ContentPlayerFactory
from contents.models import Content
from owner.models import Owner
from things.factories import ItemFactory
from .factories import GameFactory
from .models import Game
from .serializers import GameSerializer


class GameTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.game = GameFactory.create()
        owner = Owner(player=self.player, game=self.game)
        owner.save()

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

    def test_game_create_unauthorized(self):
        response = self.client.post('/game/', self.data)
        self.assertEqual(response.status_code, 401)

    def test_game_create_bad_request_1(self):
        self.data['preferences']['vision_distance'] = 'bad'
        self.authenticate()
        response = self.client.post('/game/', self.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('preferences' in response.json())
        self.assertTrue('vision_distance' in response.json().get('preferences'))

    def test_game_create_bad_request_2(self):
        self.data['start'] = 'bad'
        self.authenticate()
        response = self.client.post('/game/', self.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('start' in response.json())

    def test_game_create(self):
        games_amount = Game.objects.count()
        owners_amount = Owner.objects.count()

        self.authenticate()
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
        self.authenticate()
        response = self.client.delete('/game/{}/'.format(self.game.pk))
        self.assertEqual(response.status_code, 204)

    def test_game_update_unauthorized(self):
        self.data['preferences']['vision_distance'] = 80
        response = self.client.put('/game/{}/'.format(self.game.pk), self.data)
        self.assertEqual(response.status_code, 401)

    def test_game_update_bad_request_1(self):
        self.authenticate()
        self.data['preferences']['vision_distance'] = True
        response = self.client.put('/game/{}/'.format(self.game.pk), self.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('preferences' in response.json())
        self.assertTrue('vision_distance' in response.json().get('preferences'))

    def test_game_update_bad_request_2(self):
        self.authenticate()
        self.data['start'] = 'bad'
        response = self.client.put('/game/{}/'.format(self.game.pk), self.data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('start' in response.json())

    def test_game_update(self):
        self.authenticate()
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

    def test_game_update_partial(self):
        self.authenticate()
        data = {'description': 'other', 'preferences': {'vision_distance': 80}}
        response = self.client.patch('/game/{}/'.format(self.game.pk), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('description' in response.json().keys())
        self.assertEqual(response.json()['description'], data['description'])
        self.assertTrue('preferences' in response.json().keys())
        self.assertTrue('vision_distance' in response.json()['preferences'])
        self.assertEqual(
            response.json()['preferences']['vision_distance'],
            data['preferences']['vision_distance']
        )


class GameContentTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.item = ItemFactory.create()

        self.ct_player = ContentType.objects.get(model='player').pk
        self.ct_npc = ContentType.objects.get(model='npc').pk
        self.ct_item = ContentType.objects.get(model='item').pk
        self.ct_knowledge = ContentType.objects.get(model='knowledge').pk
        self.ct_rol = ContentType.objects.get(model='rol').pk

    def test_create_game_contents(self):
        self.authenticate()

        # Complete GAME in JSON
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
                    'content_type': self.ct_knowledge,
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
                    'content_type': self.ct_item,
                    'content_id': self.item.pk,
                    'position': {
                        'longitude': 37.201421,
                        'latitude': -6.9447224
                    },
                },
            ]
        }

        # Create game in parts

        ## Create game
        response = self.client.post('/game/', data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.json().keys())
        game_id = response.json().get('id')
        self.assertEqual(Game.objects.count(), 1)

        ## Create contents
        for content in data.pop('contents'):
            content.update({'game': game_id})
            response = self.client.post('/content/', content)
            self.assertEqual(response.status_code, 201)
        self.assertEqual(Content.objects.count(), 3)


class PlayerJoinToGameTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.game = GameFactory.create()

        self.ct_player = ContentType.objects.get(model='player').pk
        self.ct_npc = ContentType.objects.get(model='npc').pk
        self.ct_item = ContentType.objects.get(model='item').pk
        self.ct_knowledge = ContentType.objects.get(model='knowledge').pk
        self.ct_rol = ContentType.objects.get(model='rol').pk
        self.data = {
            'position': {
                'longitude': 37.201421,
                'latitude': -6.9447224
            }
        }

    def test_player_join_to_game_without_autentication(self):
        response = self.client.post('/game/{}/join/'.format(self.game.pk),
                                    self.data)
        self.assertEqual(response.status_code, 401)

    def test_player_join_to_game_content_not_exist(self):
        self.authenticate()
        response = self.client.post('/game/{}/join/'.format(self.game.pk),
                                    self.data)
        self.assertEqual(response.status_code, 201)

    def test_player_join_to_game_content_exist(self):
        self.authenticate()
        ContentPlayerFactory.create(game_id=self.game.pk, content=self.player)
        response = self.client.post('/game/{}/join/'.format(self.game.pk),
                                    self.data)
        self.assertEqual(response.status_code, 200)

    def test_player_join_to_game_game_not_exist(self):
        self.authenticate()
        response = self.client.post('/game/{}/join/'.format(self.game.pk + 1),
                                    self.data)
        self.assertEqual(response.status_code, 404)

    def test_player_join_bad_requests(self):
        self.authenticate()
        data = {'pos': {}}
        response = self.client.post('/game/{}/join/'.format(self.game.pk), data)
        self.assertEqual(response.status_code, 400)

        data = {'position': {'latitude': -6.9447224}}
        response = self.client.post('/game/{}/join/'.format(self.game.pk), data)
        self.assertEqual(response.status_code, 400)
