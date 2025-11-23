from dataclasses import dataclass
from repository import UserRepository
from schema import UserLoginSchema
from random import choice
from service.auth import AuthService
import string


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService


    def create_user(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.create_user(username, password)
        access_token=self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)




