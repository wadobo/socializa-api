from django.core.management import call_command
from rest_framework.test import APITestCase

from .client import BaseClient
from character.factories import PlayerFactory
from character.models import Player


class BaseTestCase(APITestCase):

    def setUp(self):
        call_command('socialapps')
        self.client = BaseClient()
        self.player = PlayerFactory.create()

    def tearDown(self):
        self.client = None
        Player.objects.all().delete()

    def test_authenticate(self):
        pwd = 'qweqweqwe'
        response = self.client.authenticate(self.player.user.username, pwd)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.client.auth_token, '')
        self.assertEqual(
            sorted(list(response.json().keys())),
            sorted(['access_token', 'expires_in', 'refresh_token', 'scope',
                    'token_type']),
        )

    def test_logout_without_login(self):
        response = self.client.logout()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'error': 'invalid_request',
                'error_description': 'Missing token parameter.'
            }
        )

    def test_logout(self):
        pwd = 'qweqweqwe'
        self.client.authenticate(self.player.user.username, pwd)
        response = self.client.logout()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.client.auth_token, '')
