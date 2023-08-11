import pytest
from django.core import mail
from django.contrib.auth.models import User
from model_bakery import baker
from app.views import test_send_email
from rest_framework.test import APIClient
from urllib.parse import quote
from django.test import override_settings, modify_settings
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from django.urls import reverse


@pytest.fixture
def api_client():
    return APIClient()

def test_email():
    test_send_email()
    print('Количество сообщений:',len(mail.outbox))
    outbox = mail.outbox[0]
    print('Заголовок:',outbox.subject)
    print('Сообщение:',outbox.body)
    print('От:',outbox.from_email)
    print('Кому:',outbox.to)

def test_connection(api_client):
    response = api_client.get('')
    assert response.status_code == 200


@pytest.mark.django_db
class TestUser:

    def test_registration(self,api_client):
        data = {'username':'username',
                'password':'password',
                'email':'test@email.com',
                'company':'company',
                'position':'position'}
        response = api_client.post('/api/user/',data)
        print (response)
        token = api_client.post(
            '/api/token/',
            {
                'email':data['email'],
                'password':data['password'],
                }).json()['access']

#       response = api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        headers = {
            "Authorization": f"Bearer {token}"}
        
        response = api_client.get('/api/user/1/', headers=headers).json()

        assert response['id'] == 1
        assert response['username'] == 'username'
        assert check_password(data['password'],response['password'])


