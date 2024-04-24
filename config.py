from dotenv import load_dotenv
import os


#загрузка переменных окружения

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")
DB_HOST = os.environ.get("DB_HOST")

token = os.environ.get("TOKEN")