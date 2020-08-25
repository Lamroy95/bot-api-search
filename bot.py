#!venv/bin/python
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import API_TOKEN
from get_articles import get_api_articles, get_aiogram_examples
import hashlib
import logging


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
@dp.throttled(rate=2)
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm bot that searches articles from Telegram Bot API and Aiogram framework examples!\nInline mode only:\n<code>@tgapisearchbot</code> query\n\n<i>Powered by aiogram</i>")


@dp.inline_handler(lambda q: len(q.query) > 2 and len(q.query) < 60)
async def fetch_inline(inline_query: types.InlineQuery):
    text = inline_query.query
    if not text:
        return

    items = []

    # add results from TG Bot API Reference
    api_results = await get_api_articles(text)
    # add results from docs (?)
    xmpl_results = await get_aiogram_examples(text)
    results = (api_results or []) + (xmpl_results or [])
    # check results
    if not results:
        return

    # 50 results max
    for res in results[:50]:
        result_id = hash(res['title'])
        input_content = types.InputTextMessageContent(
            f'{res["type"]}: <a href=\"{res["link"]}\">{res["title"]}</a>',
            disable_web_page_preview=True
        )
        if res['type'] == 'API Reference':
            thumb_url = 'https://telegram.org/img/t_logo.png'
        else:
            thumb_url = 'https://docs.aiogram.dev/en/latest/_static/logo.png'
        item = types.InlineQueryResultArticle(
            id=result_id,
            title=res["title"],
            description=res["type"],
            input_message_content=input_content,
            thumb_url=thumb_url
        )
        items.append(item)

    await bot.answer_inline_query(inline_query.id, results=items, cache_time=240)


@dp.inline_handler(lambda q: len(q.query) < 3)
async def default_handler(inline_query: types.InlineQuery):
    telegram_thumb_url = 'https://telegram.org/img/t_logo.png'
    aiogram_thumb_url = 'https://docs.aiogram.dev/en/latest/_static/logo.png'

    item1 = types.InlineQueryResultArticle(
        id=1,
        title="Telegram Bot API Reference",
        input_message_content=types.InputTextMessageContent(
            '<a href="https://core.telegram.org/bots/api">Telegram Bot API Reference</a>',
            disable_web_page_preview=True
        ),
        thumb_url=telegram_thumb_url
    )

    item2 = types.InlineQueryResultArticle(
        id=2,
        title="Aiogram Documentation",
        input_message_content=types.InputTextMessageContent(
            '<a href="https://docs.aiogram.dev/en/latest/">Aiogram Documentation</a>',
            disable_web_page_preview=True
        ),
        thumb_url=aiogram_thumb_url
    )

    item3 = types.InlineQueryResultArticle(
        id=3,
        title="Aiogram Sources",
        input_message_content=types.InputTextMessageContent(
            '<a href="https://github.com/aiogram/aiogram/">Aiogram Sources</a>',
            disable_web_page_preview=True
        ),
        thumb_url=aiogram_thumb_url
    )

    await bot.answer_inline_query(inline_query.id, results=[item1, item2, item3], cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
