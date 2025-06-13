from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # This tells Pydantic to load variables from the .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Define ALL your environment variables here
    GROQ_API_KEY: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_ROOT_PASSWORD: str
    KEYCLOAK_SERVER_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str
    KEYCLOAK_ADMIN_USER: str
    KEYCLOAK_ADMIN_PASSWORD: str

# Create a single instance of the settings to be used throughout the app
settings = Settings()