from dataclasses import dataclass
from repository import UserRepository
from schema import UserLoginSchema, UserCreateSchema
from random import choice
from service.auth import AuthService
import string


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService


    async def create_user(self, username: str, password: str) -> UserLoginSchema:
        user_data = UserCreateSchema(username=username, password=password)
        user = await self.user_repository.create_user(user_data)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)




