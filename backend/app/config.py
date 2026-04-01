import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "development")
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")


settings = Settings()