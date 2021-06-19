#!venv/bin/python
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from advantages import get_advantages_article
import config
from searcher import searcher
from metrics import send_metric, MetricsMiddleware


logging.basicConfig(level=logging.DEBUG)


bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def send_welcome(message: types.Message):
    await message.reply(
        "Hello.\nI'm an inline bot that searches articles from Telegram Bot API and Aiogram framework examples!\n"
        f"Inline mode only: <code>@{(await bot.me).username} search_query</code>\n"
        "<i>Powered by aiogram</i>"
    )


@dp.inline_handler(lambda q: 2 < len(q.query) < 30)
async def fetch_inline(inline_query: types.InlineQuery):
    text = inline_query.query
    items = []
    api_articles = await searcher.get_api_articles(text)
    examples = await searcher.get_aiogram_examples(text)
    results = api_articles + examples
    offset = int(inline_query.offset or 0)

    for article in results[offset:offset+config.MAX_INLINE_RESULTS]:
        result_id = article['title']
        while len(article['title'].encode('utf-8')) > 64:
            result_id = result_id[:-1]

        input_content = types.InputTextMessageContent(
            f'{article["type"]}: <a href=\"{article["link"]}\">{article["title"]}</a>',
            disable_web_page_preview=True
        )
        item = types.InlineQueryResultArticle(
            id=result_id,
            title=article["title"],
            description=article["type"],
            input_message_content=input_content
        )
        items.append(item)

    next_offset = str(offset + config.MAX_INLINE_RESULTS) if len(items) == config.MAX_INLINE_RESULTS else ""
    await bot.answer_inline_query(
        inline_query.id,
        results=items,
        cache_time=config.QUERY_CACHE_TIME,
        next_offset=next_offset,
    )


# default inline results
@dp.inline_handler(lambda q: len(q.query) < 3)
async def default_handler(inline_query: types.InlineQuery):
    item1 = types.InlineQueryResultArticle(
        id="api-reference",
        title="Telegram Bot API Reference",
        input_message_content=types.InputTextMessageContent(
            '<a href="https://core.telegram.org/bots/api">Telegram Bot API Reference</a>',
            disable_web_page_preview=True),
        thumb_url=config.TG_LOGO_URL
    )

    item2 = types.InlineQueryResultArticle(
        id="aiogram-examples",
        title="Aiogram Examples",
        input_message_content=types.InputTextMessageContent(
            '<a href="https://github.com/aiogram/aiogram/tree/dev-2.x/examples">Aiogram Examples</a>',
            disable_web_page_preview=True),
        thumb_url=config.AIOGRAM_LOGO_URL
    )

    item3 = types.InlineQueryResultArticle(
        id="why-aiogram",
        title="Почему aiogram?",
        input_message_content=types.InputTextMessageContent(
            await get_advantages_article(),
            disable_web_page_preview=True)
    )
    await bot.answer_inline_query(
        inline_query.id,
        results=[item1, item2, item3],
        cache_time=config.QUERY_CACHE_TIME,
        switch_pm_text="Query should be >3 characters",
        switch_pm_parameter="must_click",
    )


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    send_metric(
        measurement="errors",
        tags=dict(),
        fields={
            "error_message": str(exception)
        }
    )

    await bot.send_message(
        config.LOG_CHAT_ID,
        f"Cause exception <b>{exception}</b> in update\n<code>{update}</code>"
    )
    return True


async def notify_startup(*args):
    await bot.send_message(config.LOG_CHAT_ID, "Bot started")


async def notify_shutdown(*args):
    await bot.send_message(config.LOG_CHAT_ID, "Bot stopped")


if __name__ == '__main__':
    dp.middleware.setup(MetricsMiddleware())
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=notify_startup,
        on_shutdown=notify_shutdown,
    )
