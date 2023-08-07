import pytest
from django.contrib.auth.models import User
from model_bakery import baker

from rest_framework.test import APIClient
from urllib.parse import quote
from django.test import override_settings, modify_settings
from rest_framework import serializers


@pytest.fixture
def api_client():
    return APIClient()


def test_connection(api_client):
    response = api_client.get('')
    assert response.status_code == 200

@pytest.mark.django_db
class TestUser:

    def test_post(self,api_client):
        data = {'username':'username',
                'password':'password',
                'email':'test@email.com',
                'company':'company',
                'position':'position'}
        response = api_client.post('/api/user/',data)
        response = api_client.get('/api/user/1/').json()

        assert response['id'] == 1
        assert response['username'] == 'username'
        assert response['password']


