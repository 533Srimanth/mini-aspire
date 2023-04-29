import pytest
import factory

from exceptions import AuthorizationError, AuthFailedException, AuthHeaderMissingException, EntityDoesNotExistException


@pytest.fixture
def user_controller():
    return factory.initialize_one('user_controller')


@pytest.fixture
def dummy_user():
    return {
        "name": "Srimanth",
        "email": "533srimanth@gmail.com",
        "password": "password"
    }


def test_user_signup(user_controller, dummy_user):
    user = user_controller._signup(dummy_user)
    assert user.name == dummy_user['name']
    assert user.email == dummy_user['email']

    user = user_controller.user_service.fetch_by_id(user.id)
    assert user.password_hash == hash(dummy_user['password'])


def test_user_login(user_controller, dummy_user):
    user = user_controller._signup(dummy_user)
    user_login_response = user_controller._login(dummy_user)

    assert user_login_response.message == "Success"
    assert user_login_response.token is not None
    assert user_login_response.user == user

    with pytest.raises(EntityDoesNotExistException):
        user_controller._login({'email': 'random-email', 'password': 'pw'})


def test_fetch_all_users(user_controller, dummy_user):
    user_controller._signup(dummy_user)
    user_controller._signup(dummy_user)
    user_controller._signup(dummy_user)

    users = user_controller._fetch_all(headers={'x-admin-auth-token': 'admin-token'})
    assert users.message == "Success"
    assert users.count == 3


def test_fetch_all_users_auth_fail(user_controller, dummy_user):
    user_controller._signup(dummy_user)
    user_controller._signup(dummy_user)
    user_controller._signup(dummy_user)

    with pytest.raises(Exception):
        user_controller._fetch_all(headers={'x-admin-auth-token': 'random-token'})


def test_fetch_by_id(user_controller, dummy_user):
    user_controller._signup(dummy_user)
    user_login_response = user_controller._login(dummy_user)

    user = user_controller._fetch(headers={'x-auth-token': user_login_response.token}, id=user_login_response.user.id)
    assert user == user_login_response.user


def test_fetch_by_id_auth_fail(user_controller, dummy_user):
    user_controller._signup(dummy_user)
    user_login_response = user_controller._login(dummy_user)

    with pytest.raises(AuthFailedException):
        user_controller._fetch(headers={'x-auth-token': 'random-token'}, id=user_login_response.user.id)
    with pytest.raises(AuthHeaderMissingException):
        user_controller._fetch(headers={}, id=user_login_response.user.id)

    user2 = user_controller._signup({'name': 'user2', 'email': 'email2', 'password': 'pw'})
    token2 = user_controller._login({'email': user2.email, 'password': 'pw'}).token
    with pytest.raises(AuthorizationError):
        user_controller._fetch(headers={'x-auth-token': token2}, id=user_login_response.user.id)
