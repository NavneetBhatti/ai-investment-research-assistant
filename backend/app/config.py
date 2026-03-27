import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "development")


settings = Settings()