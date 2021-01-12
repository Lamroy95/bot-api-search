from os import environ
from dotenv import load_dotenv


load_dotenv(verbose=True)


API_TOKEN = environ.get("API_TOKEN")
LOG_CHAT_ID = environ.get("LOG_CHAT_ID")

TG_LOGO_URL = 'https://telegram.org/img/t_logo.png'
AIOGRAM_LOGO_URL = 'https://docs.aiogram.dev/en/latest/_static/logo.png'
MAX_INLINE_RESULTS = 50
QUERY_CACHE_TIME = 120
