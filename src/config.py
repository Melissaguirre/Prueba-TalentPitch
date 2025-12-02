from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the application.
    """

    SENDGRID_API_KEY: str
    EMAIL_SENDER: str
    EMAIL_RECEIVER: str
    TEMPLATE_ID: str

    class Config:
        env_file = ".env"
    
settings: Settings = Settings()
