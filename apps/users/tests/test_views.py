import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.test.client import Client

from ..models import UserRoleChoices, CustomUserModel

test_user_data = {'email': '10@gmial.com', 'name': 'name_10', 'password': 'pass_1'}
employee_data = {'email': 'employee@gmial.com', 'name': 'employee', 'password': 'employee',
                 'role': 'em', 'is_active': True}
rest_admin_data = {'email': 'rest_admin@gmial.com', 'name': 'rest_admin', 'password': 'rest_admin',
                   'role': 'ra', 'is_active': True}
admin_data = {'email': 'admin@gmail.com', 'name': 'admin', 'password': 'admin', 'role': 'ad'}


@pytest.fixture
def admin(db):
    admin = CustomUserModel.objects.create_superuser(**admin_data)
    return admin


@pytest.fixture
def employee(db):
    employee = CustomUserModel.objects.create_user(**employee_data)
    return employee


@pytest.fixture
def rest_admin(db):
    rest_admin = CustomUserModel.objects.create_user(**rest_admin_data)
    return rest_admin


@pytest.fixture()
def login_as_rest_admin(rest_admin):
    refresh = RefreshToken.for_user(user=rest_admin)
    return {'access': str(refresh.access_token), 'refresh': str(refresh)}


@pytest.fixture()
def admin_client(admin):
    refresh = RefreshToken.for_user(user=admin)
    credentials = {'access': str(refresh.access_token), 'refresh': str(refresh)}

    client = Client(HTTP_AUTHORIZATION=f'Bearer {credentials["access"]}')
    return client


@pytest.fixture()
def employee_client(employee):
    refresh = RefreshToken.for_user(user=employee)
    credentials = {'access': str(refresh.access_token), 'refresh': str(refresh)}

    client = Client(HTTP_AUTHORIZATION=f'Bearer {credentials["access"]}')
    return client


@pytest.fixture()
def rest_admin_client(rest_admin):
    refresh = RefreshToken.for_user(user=rest_admin)
    credentials = {'access': str(refresh.access_token), 'refresh': str(refresh)}

    client = Client(HTTP_AUTHORIZATION=f'Bearer {credentials["access"]}')
    return client


def test_admin_user_create_with_wrong_status(client, db):
    data = admin_data.copy()
    data['is_active'] = False
    with pytest.raises(ValueError) as e:
        CustomUserModel.objects.create_superuser(**data)

    assert str(e.value) == 'User has to be active.'


def test_admin_user_create_with_wrong_role(client, db):
    data = admin_data.copy()
    data['role'] = 'em'
    with pytest.raises(ValueError) as e:
        CustomUserModel.objects.create_superuser(**data)

    assert str(e.value) == 'User role has to be \'administrator\'.'


def test_user_register(client, db):
    url = reverse('register_new_user')
    test_user_data['role'] = str(UserRoleChoices.RESTAURANT_ADMINISTRATOR.label)
    response = client.post(path=url, data=test_user_data)

    assert response.status_code == 201


@pytest.mark.parametrize(
    'user_data',
    [admin_data, employee_data, rest_admin_data]
)
def test_user_login_when_user_not_exists(user_data, client, db):
    url = reverse('get_token_pair')
    credentials = {'email': user_data['email'], 'password': user_data['password']}
    response = client.post(url, data=credentials)

    assert response.status_code == 401


@pytest.mark.parametrize(
    'user_data',
    [employee_data, rest_admin_data]
)
def test_user_login_when_user_exists(user_data, client, db):
    url = reverse('get_token_pair')
    CustomUserModel.objects.create_user(**user_data)

    credentials = {'email': user_data['email'], 'password': user_data['password']}
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


def test_get_all_users_with_admin_authorization_creds(admin_client):
    url = reverse('get_all_users')
    response = admin_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)


def test_get_all_active_users(admin_client):
    url = reverse('get_all_users')
    url = url + '?is_active=True'
    response = admin_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 1


def test_get_all_non_active_users(admin_client, db):
    url = reverse('get_all_users')
    url = url + '?is_active=False'
    test_user_data['role'] = 'em'
    CustomUserModel.objects.create_user(**test_user_data)
    response = admin_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 1


def test_get_all_users_with_employee_authorization_creds(employee_client):
    url = reverse('get_all_users')
    response = employee_client.get(url)

    assert response.status_code == 403
    assert str(response.data['detail']) == 'You do not have permission to perform this action.'


def test_get_all_users_with_rest_admin_authorization_creds(employee_client):
    url = reverse('get_all_users')
    response = employee_client.get(url)

    assert response.status_code == 403
    assert str(response.data['detail']) == 'You do not have permission to perform this action.'
