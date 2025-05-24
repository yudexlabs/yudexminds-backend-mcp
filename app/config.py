import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables del .env

class Config:
    PORT = os.getenv('PORT')
    ENV = os.getenv('ENV')
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodburi")
    MONGODB_DBNAME = os.getenv("MONGODB_DBNAME", "ideas_db")

