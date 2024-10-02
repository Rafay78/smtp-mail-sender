from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    sender_email: str 
    email_password: str 
    smtp_server_name: str
    database_hostname : str

    class Config:
        env_file = ".env"

settings = Settings()
