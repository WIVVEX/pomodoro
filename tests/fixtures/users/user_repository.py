import pytest
from dataclasses import dataclass

from app.users.user_profile.models import UserProfile
from app.users.user_profile.schema import UserCreateSchema
from tests.fixtures.users.user_model import UserProfileFactory


@dataclass
class FakeUserRepository():

    async def get_user_by_email(self, email: str) -> None:
        return None

    async def create_user(self, user_data: UserCreateSchema):
        return UserProfileFactory(
            id="123",
            username="FakeUsername",
            password="FakePassword",
            email="test@example.com",
            name="Test Name")
    
    async def get_user_by_username(self, username: str) -> UserProfile:
        if username == "FakeUsername":
            return UserProfileFactory(
                id="123",
                username="FakeUser",
                password="FakePassword",
                email="test@example.com",
                name="Test Name")
    


@pytest.fixture
def user_repository():
    return FakeUserRepository()