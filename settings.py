from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pomodoro_sql = "pomodoro.sqlite"
    