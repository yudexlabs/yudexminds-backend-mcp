import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables del .env

class Config:
    PORT: str | None = os.getenv('PORT')
    ENV: str | None = os.getenv('ENV')
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodburi")
    MONGODB_DBNAME: str = os.getenv("MONGODB_DBNAME", "ideas_db")
    BEARER_TOKEN_MCP: str = os.getenv("BEARER_TOKEN_MCP", "supersecreto123")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "un_secret_muy_seguro")
    USERNAME_MOCKUP_USER = os.getenv("USERNAME_MOCKUP_USER", "")
    PASSWORD_MOCKUP_USER = os.getenv("PASSWORD_MOCKUP_USER", "")

