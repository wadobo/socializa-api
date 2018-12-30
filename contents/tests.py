from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import Point
from django.core.management import call_command

from base.tests import BaseTestCase
from character.factories import PlayerFactory
from character.models import NPC
from game.factories import GameFactory
from game.models import Game
from owner.models import Owner
from things.factories import ItemFactory
from things.models import Item, Knowledge, Rol
from .models import Content
from .factories import (
    ContentPlayerFactory,
    ContentNPCFactory,
    ContentItemFactory,
    ContentKnowledgeFactory,
    ContentRolFactory,
)
from .serializers import ContentSerializer


class ContentTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.game = GameFactory.create()
        owner = Owner(player=self.player, game=self.game)
        owner.save()
        self.content_player = ContentPlayerFactory.create(game_id=self.game.pk)
        self.content_npc = ContentNPCFactory.create(game_id=self.game.pk)
        self.content_item = ContentItemFactory.create(
            game_id=self.game.pk,
            position=Point(37.261421, -6.9447224)
        )
        self.content_knowledge = ContentKnowledgeFactory.create(game_id=self.game.pk)
        self.content_rol = ContentRolFactory.create(game_id=self.game.pk)
        self.item = ItemFactory.create()

        self.data_mode1 = {
            "game": self.game.pk,
            "position": {
                "longitude": 37.261421,
                "latitude": -6.9447224
            },
            "content_type": self.content_item.content_type.pk,
            "content_id": self.item.pk,
        }

        self.data_mode2 = {
            "game": self.game.pk,
            "position": {
                "longitude": 37.261421,
                "latitude": -6.9447224
            },
            "content_type": self.content_item.content_type.pk,
            "content_id": 0,
            "content": {
                "name": "key",
                "description": "key number 1",
                "pickable": True,
                "shareable": False,
                "consumable": False,
            }
        }

    def tearDown(self):
        super().tearDown()
        NPC.objects.all().delete()
        Game.objects.all().delete()
        Owner.objects.all().delete()
        Content.objects.all().delete()
        Item.objects.all().delete()
        Knowledge.objects.all().delete()
        Rol.objects.all().delete()

    # LIST
    def test_list_content_unauth(self):
        response = self.client.get('/content/')
        self.assertEqual(response.status_code, 401)

    def test_list_content(self):
        self.authenticate()
        response = self.client.get('/content/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

    def test_list_content_filter_game(self):
        self.authenticate()
        response = self.client.get('/content/?game_id={}'.format(self.game.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

        response = self.client.get('/content/?game_id={}'.format(self.game.pk + 1))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_list_content_filter_bad(self):
        """ If you use bad query params, return none """
        self.authenticate()
        response = self.client.get('/content/?game_id=str')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

        response = self.client.get('/content/?game_pk=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    # CREATE
    def test_create_content_unauth(self):
        response = self.client.post('/content/', self.data_mode1)
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/content/', self.data_mode2)
        self.assertEqual(response.status_code, 401)

    def test_create_content_bad_request(self):
        self.authenticate()
        self.data_mode1['content_type'] = 'bad'
        response = self.client.post('/content/', self.data_mode1)
        self.assertEqual(response.status_code, 400)

        self.data_mode2['content_type'] = 'bad'
        response = self.client.post('/content/', self.data_mode2)
        self.assertEqual(response.status_code, 400)

    def test_create_content(self):
        self.authenticate()
        response = self.client.post('/content/', self.data_mode1)
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/content/', self.data_mode2)
        self.assertEqual(response.status_code, 201)

    # DESTROY
    def test_destroy_content_unauth(self):
        response = self.client.delete('/content/{}/'.format(self.content_item.pk))
        self.assertEqual(response.status_code, 401)

        player = PlayerFactory.create()
        self.client.authenticate(player.user.username, 'qweqweqwe')
        response = self.client.delete('/content/{}/'.format(self.content_item.pk))
        self.assertEqual(response.status_code, 404)

    def test_destroy_content(self):
        self.authenticate()
        response = self.client.delete('/content/{}/'.format(self.content_item.pk))
        self.assertEqual(response.status_code, 204)

    # UPDATE
    def test_update_content_unauth(self):
        data = {
            "position": {
                "longitude": 36.261421,
                "latitude": -7.9447224
            }
        }
        _url = '/content/{}/'.format(self.content_npc.pk)
        response = self.client.put(_url, data)
        self.assertEqual(response.status_code, 401)

    def test_update_content_bad_request(self):
        self.authenticate()
        data = {
            "portion": {
                "longitude": 36.261421,
                "latitude": -7.9447224
            }
        }
        _url = '/content/{}/'.format(self.content_npc.pk)
        response = self.client.put(_url, data)
        self.assertEqual(response.status_code, 400)

        data = {"position": 'bad'}
        _url = '/content/{}/'.format(self.content_npc.pk)
        response = self.client.put(_url, data)
        self.assertEqual(response.status_code, 400)

    def test_update_content(self):
        self.authenticate()
        data = ContentSerializer(self.content_npc).data
        data.update({
            "position": {
                "longitude": 36.261421,
                "latitude": -7.9447224
            }
        })
        _url = '/content/{}/'.format(self.content_npc.pk)
        response = self.client.put(_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('position'), data.get('position'))

        data = ContentSerializer(self.content_npc).data
        data.pop('position')
        data.update({
            "content_type": self.content_item.content_type.pk,
            "content_id": self.item.pk,
        })
        _url = '/content/{}/'.format(self.content_npc.pk)
        response = self.client.put(_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('content_type'),
                         data.get('content_type'))
        self.assertEqual(response.json().get('content_id'),
                         data.get('content_id'))

    # RETRIEVE
    def test_get_content_unexist_pk(self):
        self.authenticate()
        response = self.client.get('/content/{}/'.format(0))
        self.assertEqual(response.status_code, 404)

    def test_get_content_unauth(self):
        response = self.client.get('/content/{}/'.format(self.content_npc.pk))
        self.assertEqual(response.status_code, 401)

    def test_get_content(self):
        self.authenticate()
        contents = [
            self.content_player, self.content_npc, self.content_item,
            self.content_knowledge, self.content_rol
        ]
        for content in contents:
            response = self.client.get('/content/{}/'.format(content.pk))
            self.assertEqual(response.status_code, 200)
            self.assertTrue('position' in response.json().keys())
            self.assertTrue('content' in response.json().keys())
            self.assertEqual(response.json().get('content_type'),
                             content.content_type.pk)
