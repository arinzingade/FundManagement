
from dotenv import load_dotenv
import os

load_dotenv()  

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')