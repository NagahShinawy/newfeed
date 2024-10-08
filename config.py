import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'newfeed')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
