#!venv/bin/python
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import advantages
from config import API_TOKEN
from get_articles import searcher
import hashlib
import logging


TG_LOGO_URL = 'https://telegram.org/img/t_logo.png'
AIOGRAM_LOGO_URL = 'https://docs.aiogram.dev/en/latest/_static/logo.png'

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def get_advantages_article():
    result = f'{advantages.header}:'
    for i, item in enumerate(advantages.adv_list):
        result += f'\n{i+1}) {item}.'

    return result


@dp.message_handler(commands=['start', 'help'])
@dp.throttled(rate=0.5)
async def send_welcome(message: types.Message):
    await message.reply(
        "Hi!\nI'm bot that searches articles from Telegram Bot API and Aiogram framework examples!"
        "Inline mode only:<code>@tgApiSearchBot</code> query\n"
        "<i>Powered by aiogram</i>"
    )


@dp.inline_handler(lambda q: len(q.query) > 2 and len(q.query) < 40)
async def fetch_inline(inline_query: types.InlineQuery):
    text = inline_query.query
    if not text:
        return

    items = []

    # add articles from TG Bot API Reference
    api_articles = await searcher.get_api_articles(text)
    # add articles from github examples
    examples = await searcher.get_aiogram_examples(text)

    results = api_articles + examples

    # 50 results max
    for article in results[:50]:
        result_id = hash(article['title'])
        input_content = types.InputTextMessageContent(
            f'{article["type"]}: <a href=\"{article["link"]}\">{article["title"]}</a>',
            disable_web_page_preview=True
        )
        # if article['type'] == 'API Reference':
        #     thumb_url = TG_LOGO_URL
        # else:
        #     thumb_url = AIOGRAM_LOGO_URL
        item = types.InlineQueryResultArticle(
            id=result_id,
            title=article["title"],
            description=article["type"],
            input_message_content=input_content
            # thumb_url=thumb_url
        )
        items.append(item)

    await bot.answer_inline_query(inline_query.id, results=items, cache_time=120)


# default inline results: api reference, aiogram docs and aiogram src
@dp.inline_handler(lambda q: len(q.query) < 3)
async def default_handler(inline_query: types.InlineQuery):
    item1 = types.InlineQueryResultArticle(
        id=1,
        title="Telegram Bot API Reference",
        input_message_content=types.InputTextMessageContent(
            '<a href="https://core.telegram.org/bots/api">Telegram Bot API Reference</a>',
            disable_web_page_preview=True
        ),
        thumb_url=TG_LOGO_URL
    )

    item2 = types.InlineQueryResultArticle(
        id=2,
        title="Aiogram Documentation",
        input_message_content=types.InputTextMessageContent(
            '<a href="https://docs.aiogram.dev/en/latest/">Aiogram Documentation</a>',
            disable_web_page_preview=True
        ),
        thumb_url=AIOGRAM_LOGO_URL
    )

    item3 = types.InlineQueryResultArticle(
        id=3,
        title="Aiogram Sources",
        input_message_content=types.InputTextMessageContent(
            '<a href="https://github.com/aiogram/aiogram/">Aiogram Sources</a>',
            disable_web_page_preview=True
        ),
        thumb_url=AIOGRAM_LOGO_URL
    )

    item4 = types.InlineQueryResultArticle(
        id=4,
        title="Почему aiogram?",
        input_message_content=types.InputTextMessageContent(
            await get_advantages_article(),
            disable_web_page_preview=True
        )
    )

    await bot.answer_inline_query(inline_query.id, results=[item1, item2, item3, item4], cache_time=120)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
