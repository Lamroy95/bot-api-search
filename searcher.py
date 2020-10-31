import aiohttp, asyncio
from lxml import html
from datetime import datetime as dt
import logging


CACHE_MAX_AGE = 120 * 60


class Searcher:
    _cached_articles: list
    _cached_examples: list
    _session: aiohttp.ClientSession

    def __init__(self):
        loop = asyncio.get_event_loop()
        self._session = aiohttp.ClientSession()
        loop.create_task(self._cache_updater())


    async def _fetch(self, session: aiohttp.ClientSession, url: str, encoding: str='utf-8') -> str:
        async with session.get(url) as response:
            return await response.text(encoding=encoding)


    async def _cache_updater(self):
        while True:
            logging.debug('Updating cache')
            self._cached_articles = await self._get_articles_from_html()
            self._cached_examples = await self._get_examples_from_html()
            await asyncio.sleep(CACHE_MAX_AGE)


    async def _get_all_articles(self) -> list:
        if not self._cached_articles:
            logging.debug('Articles cache is empty. Updating manually')
            self._cached_articles = await self._get_articles_from_html()

        return self._cached_articles


    async def _get_articles_from_html(self) -> list:
        url = 'https://core.telegram.org/bots/api'
        expr = "//a[@class='anchor']"
        results = []

        content = await self._fetch(self._session, url)

        try:
            tree = html.fromstring(content)
        except:
            return results

        for tag in tree.xpath(expr):
            res = {
                'type': 'API Reference',
                'title': tag.xpath('following-sibling::text()')[0],
                'link': '{}{}'.format(url, tag.xpath('@href')[0])
            }
            results.append(res)

        return results


    async def _get_all_examples(self) -> list:
        if not self._cached_examples:
            self._cached_examples = await self._get_examples_from_html()

        return self._cached_examples


    async def _get_examples_from_html(self) -> list:
        url = 'https://github.com/aiogram/aiogram/tree/dev-2.x/examples'
        expr = "//a[@class=$tag_class]"
        tag_class = 'js-navigation-open link-gray-dark'

        results = []
        content = await self._fetch(self._session, url)

        tree = html.fromstring(content)

        for tag in tree.xpath(expr, tag_class=tag_class):
            res = {
                'type': 'Aiogram example',
                'title': tag.xpath('text()')[0],
                'link': '{}{}'.format('https://github.com', tag.xpath('@href')[0])
            }
            results.append(res)

        return results


    async def get_api_articles(self, query: str) -> list:
        results = []
        query = query.lower()
        articles = await self._get_all_articles()

        for article in articles:
            if query in article['title']:
                results.append(article)
            elif query in article['link']:
                    results.append(article)

        return results


    async def get_aiogram_examples(self, query: str) -> list:
        results = []
        query = query.lower()
        examples = await self._get_all_examples()

        for example in examples:
            if query in example['title']:
                results.append(example)

        return results


searcher = Searcher()
