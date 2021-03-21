from os import environ
from dotenv import load_dotenv


load_dotenv(verbose=True)


API_TOKEN = environ.get("API_TOKEN")
LOG_CHAT_ID = environ.get("LOG_CHAT_ID")

TG_LOGO_URL = 'https://telegram.org/img/t_logo.png'
AIOGRAM_LOGO_URL = 'https://docs.aiogram.dev/en/latest/_static/logo.png'
MAX_INLINE_RESULTS = 50
QUERY_CACHE_TIME = 120

API_REFERENCE_URL = 'https://core.telegram.org/bots/api'
EXAMPLES_URL = 'https://github.com/aiogram/aiogram/tree/dev-2.x/examples'
CACHE_MAX_AGE = 120 * 60
EXAMPLES_ALIASES = {
    "finite_state_machine_example.py": ["fsm"],
}

API_ARTICLE_ANCHOR_XPATH = "//a[@class='anchor']"
EXAMPLES_LINK_XPATH = "//a[@class='js-navigation-open Link--primary']"
