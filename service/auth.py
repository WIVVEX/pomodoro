from dataclasses import dataclass
from jose import jwt
from jose.exceptions import JWTError
import datetime as dt
from datetime import timedelta
from models import UserProfile
from repository import UserRepository
from schema import UserLoginSchema
from exceptions import TokenExpired, TokenNotCorrect, UserNotFoundException, UserNotCorrectPasswordException
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    async def google_auth(self, code: str):
        user_data = await self.google_client.get_user_info(code)

        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            print("user_login")
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            google_access_token=user_data.access_token, 
            email=user_data.email,
            name=user_data.name
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        print("user_create")
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)
    

    async def yandex_auth(self, code: str):
        user_data = await self.yandex_client.get_user_info(code=code)
        print(user_data)
        if user := await self.user_repository.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user_id=user.id)
            print("user_login")
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            yandex_access_token=user_data.access_token, 
            email=user_data.default_email,
            name=user_data.name
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        print("user_create")
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    async def get_yandex_redirect_url(self) -> str:   
        return self.settings.yandex_redirect_url

    async def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
    

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
    

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()  
        token = jwt.encode(
            {'user_id': user_id, 'expire' : expires_date_unix}, 
            self.settings.JWT_SECRET_KEY, 
            algorithm=self.settings.JWT_ENCODE_ALGORITHM)
        return token
    
    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise TokenNotCorrect

        if payload['expire'] < dt.datetime.utcnow().timestamp():
            raise TokenExpired
        return payload["user_id"]

