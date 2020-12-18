import logging

import aiohttp
import asyncio
from lxml import html


API_REFERENCE_URL = 'https://core.telegram.org/bots/api'
EXAMPLES_URL = 'https://github.com/aiogram/aiogram/tree/dev-2.x/examples'
CACHE_MAX_AGE = 120 * 60
EXAMPLES_ALIASES = {
    "finite_state_machine_example.py": ["fsm"],
}


async def fetch(session: aiohttp.ClientSession, url: str, encoding: str = 'utf-8') -> str:
    async with session.get(url) as response:
        assert response.status == 200
        return await response.text(encoding=encoding)


class Searcher:
    _cached_articles: list
    _cached_examples: list
    _session: aiohttp.ClientSession

    def __init__(self):
        loop = asyncio.get_event_loop()
        self._session = aiohttp.ClientSession()
        loop.create_task(self._cache_updater())

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
        expr = "//a[@class='anchor']"
        results = []

        content = await fetch(self._session, API_REFERENCE_URL)

        tree = html.fromstring(content)

        for tag in tree.xpath(expr):
            res = {
                'type': 'API Reference',
                'title': tag.xpath('following-sibling::text()')[0],
                'link': '{}{}'.format(API_REFERENCE_URL, tag.xpath('@href')[0])
            }
            results.append(res)

        return results

    async def _get_all_examples(self) -> list:
        if not self._cached_examples:
            self._cached_examples = await self._get_examples_from_html()

        return self._cached_examples

    async def _get_examples_from_html(self) -> list:
        results = []
        content = await fetch(self._session, EXAMPLES_URL)
        tree = html.fromstring(content)

        expr = "//a[@class=$tag_class]"
        tag_class = 'js-navigation-open link-gray-dark'
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
            if query in example['title'] or query in EXAMPLES_ALIASES.get(example['title'], []):
                results.append(example)

        return results


searcher = Searcher()
