import pytest
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken

from ..models import UserRoleChoices, CustomUserModel

test_user_data = {'email': '10@gmial.com', 'name': 'name_10', 'password': 'pass_1'}
admin_data = {'email': 'admin@gmail.com', 'name': 'admin', 'password': 'pass'}


@pytest.fixture
def create_admin(db):
    user = CustomUserModel.objects.create_superuser(**admin_data)
    return user


@pytest.fixture()
def login_as_admin(create_admin):
    refresh = RefreshToken.for_user(user=create_admin)
    return {'access': str(refresh.access_token), 'refresh': str(refresh)}


def test_user_register(client, db):
    url = reverse('register_new_user')
    test_user_data['role'] = str(UserRoleChoices.RESTAURANT_ADMINISTRATOR.label)
    response = client.post(path=url, data=test_user_data)

    assert response.status_code == 201


def test_admin_login(create_admin, client):
    url = reverse('get_token_pair')
    credentials = {'email': admin_data['email'], 'password': admin_data['password']}
    response = client.post(url, data=credentials)

    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data


def test_login_with_wrong_data(client, db):
    url = reverse('get_token_pair')
    credentials = {'email': test_user_data['email'], 'password': test_user_data['password']}
    response = client.post(url, data=credentials)

    assert response.status_code == 401


def test_get_all_users_without_authorization(client, db):
    url = reverse('get_all_users')
    response = client.get(url)

    assert response.status_code == 401

