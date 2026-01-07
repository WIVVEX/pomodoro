import pytest
from app.exceptions import UserNotCorrectPasswordException, UserNotFoundException
from app.settings import Settings
from app.users.auth.schema import UserLoginSchema
from app.users.auth.service import AuthService
from jose import jwt
import datetime as dt
from app.users.user_profile.models import UserProfile
pytestmark = pytest.mark.asyncio

async def test_get_google_redirect_url__success(mock_auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = settings.google_redirect_url
    auth_service_mock_google_redirect_url = mock_auth_service.get_google_redirect_url()
    assert settings_google_redirect_url == auth_service_mock_google_redirect_url


async def test_get_yandex_redirect_url__success(mock_auth_service: AuthService, settings: Settings):
    settings_yandex_redirect_url = settings.yandex_redirect_url
    auth_service_mock_yandex_redirect_url = mock_auth_service.get_yandex_redirect_url()
    assert settings_yandex_redirect_url == auth_service_mock_yandex_redirect_url


async def test_get_google_redirect_url__fail(mock_auth_service: AuthService):
    settings_google_redirect_url = "https://fake_google_redirect_url.com"
    auth_service_mock_google_redirect_url = mock_auth_service.get_google_redirect_url()
    assert settings_google_redirect_url != auth_service_mock_google_redirect_url

async def test_get_yandex_redirect_url__fail(mock_auth_service: AuthService):
    settings_yandex_redirect_url = "https://fake_yandex_redirect_url.com"
    auth_service_mock_yandex_redirect_url = mock_auth_service.get_yandex_redirect_url()
    assert settings_yandex_redirect_url != auth_service_mock_yandex_redirect_url

async def test_generate_access_token__success(mock_auth_service: AuthService, settings: Settings):
    user_id = str(1)
    access_token = mock_auth_service.generate_access_token(user_id=user_id)
    decoded_access_token = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ENCODE_ALGORITHM])
    decoded_user_id = decoded_access_token.get("user_id")
    decoded_token_expire = dt.datetime.fromtimestamp(decoded_access_token.get("expire"), tz=dt.timezone.utc)
    
    assert (decoded_token_expire - dt.datetime.now(tz=dt.UTC)) > dt.timedelta(days=6)
    assert decoded_user_id == user_id


async def test_get_user_id_from_access_token__success(mock_auth_service: AuthService):
    user_id = str(1)

    access_token = mock_auth_service.generate_access_token(user_id=user_id)
    decoded_user_id = mock_auth_service.get_user_id_from_access_token(access_token)

    assert str(decoded_user_id) == str(user_id)

async def test_google_auth__success(mock_auth_service: AuthService):
    code = "fake_code"
    
    user = await mock_auth_service.google_auth(code=code)
    decoded_user_id = mock_auth_service.get_user_id_from_access_token(user.access_token)

    assert str(user.user_id) == str(decoded_user_id)
    assert isinstance(user, UserLoginSchema)


async def test_yandex_auth__success(mock_auth_service: AuthService):
    code = "fake_code"
    
    user = await mock_auth_service.yandex_auth(code=code)
    decoded_user_id = mock_auth_service.get_user_id_from_access_token(user.access_token)

    assert str(user.user_id) == str(decoded_user_id)
    assert isinstance(user, UserLoginSchema)

async def test_validate_auth_user__success(mock_auth_service: AuthService):
    user_data = {
        "id" : "123",
        "password": "FakePassword",
        "username" : "FakeUsername"
        }
    user = await mock_auth_service.user_repository.create_user(user_data=user_data)
    assert isinstance(user, UserProfile)
    mock_auth_service._validate_auth_user(user=user, password=user_data["password"])
    
async def test_validate_auth_user__wrong_password(mock_auth_service: AuthService):
    user_data = {
        "id" : "123",
        "password": "FakePassword",
        "username" : "FakeUsername"
        }
    user = await mock_auth_service.user_repository.create_user(user_data=user_data)
    with pytest.raises(UserNotCorrectPasswordException):
        mock_auth_service._validate_auth_user(user=user, password="WrongPassword")

async def test_validate_auth_user__user_not_found(mock_auth_service: AuthService):
    user = None
    with pytest.raises(UserNotFoundException):
        mock_auth_service._validate_auth_user(user=user, password="any_password")


async def test_login__success(mock_auth_service: AuthService):
    user_data = {
        "id" : "123",
        "password": "FakePassword",
        "username" : "FakeUsername"
        }
    
    created_user = await mock_auth_service.user_repository.create_user(user_data=user_data)
    result = await mock_auth_service.login(username=user_data["username"], password=user_data["password"])
    
    assert isinstance(result, UserLoginSchema)
    print(result.user_id)
    print(created_user.id)
    assert str(result.user_id) == str(created_user.id)
    assert result.access_token is not None
    assert len(result.access_token) > 0 



async def test_login__wrong_password(mock_auth_service: AuthService):
    user_data = {
        "id" : "123",
        "password": "FakePassword",
        "username" : "FakeUsername"
        }
    
    await mock_auth_service.user_repository.create_user(user_data=user_data)
    
    with pytest.raises(UserNotCorrectPasswordException):
        await mock_auth_service.login(username="FakeUsername", password="WrongPassword")



async def test_login__user_not_found(mock_auth_service: AuthService):
    with pytest.raises(UserNotFoundException):
        await mock_auth_service.login(username="NonExistentUser", password="any")

