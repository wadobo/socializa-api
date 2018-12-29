import json

from django.conf import settings
from django.test import Client
from oauth2_provider.models import Application


class BaseClient(Client):
    def __init__(self, *args, **kwargs):
        self.auth_token = ''
        self.access_token = ''
        version = kwargs.get('version', settings.VERSION)
        self.base_url = '/api/v{0}'.format(version)
        super().__init__(*args, **kwargs)

    def set_auth_token(self, response):
        json_res = response.json()
        token_type = json_res.get('token_type')
        self.access_token = json_res.get('access_token')
        self.auth_token = '%s %s' % (token_type, self.access_token)

    def authenticate(self, email, password):
        app = Application.objects.get(name='local')
        data = {
            'client_id': app.client_id,
            'grant_type': 'password',
            'username': email,
            'password': password
        }
        response = self.post('/auth/token/', data)
        if response.status_code == 200:
            self.set_auth_token(response)
        return response

    def logout(self):
        app = Application.objects.get(name='local')
        data = {
            'client_id': app.client_id,
            'grant_type': 'password',
            'token': self.access_token
        }
        response = self.post('/auth/revoke-token/', data)
        if response.status_code == 204:
            self.auth_token = ''
        return response

    def extra(self):
        return {
            'content_type': 'application/json',
            'HTTP_AUTHORIZATION': self.auth_token
        }

    def get(self, url):
        return super().get(self.base_url + url, **self.extra())

    def post(self, url, data=None):
        data = {} if data is None else json.dumps(data)
        return super().post(self.base_url + url, data, **self.extra())

    def put(self, url, data=None):
        data = {} if data is None else json.dumps(data)
        return super().put(self.base_url + url, data, **self.extra())

    def patch(self, url, data=None):
        data = {} if data is None else json.dumps(data)
        return super().patch(self.base_url + url, data, **self.extra())

    def delete(self, url, data=None):
        data = {} if data is None else json.dumps(data)
        return super().delete(self.base_url + url, data, **self.extra())
