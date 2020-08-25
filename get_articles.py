import aiohttp
from lxml import html


async def fetch(session, url, encoding='utf-8'):
    try:
        async with session.get(url) as response:
            return await response.text(encoding=encoding)
    except Exception:
        return None


async def get_api_articles(query: str):
    url = 'https://core.telegram.org/bots/api'
    async with aiohttp.ClientSession() as session:
        content = await fetch(session, url)
    if not content:
        return None

    tree = html.fromstring(content)
    results = []
    for tag in tree.xpath("//a[contains(@href, '{}') and @class='anchor']".format(query.lower())):
        res = {}
        res['type'] = 'API Reference'
        res['title'] = tag.xpath('following-sibling::text()')[0]
        res['link'] = '{}{}'.format(url, tag.xpath('@href')[0])
        results.append(res)

    return results if results else None


async def get_aiogram_examples(query: str):
    url = 'https://github.com/aiogram/aiogram/tree/dev-2.x/examples'
    async with aiohttp.ClientSession() as session:
        content = await fetch(session, url)
    if not content:
        return None

    tree = html.fromstring(content)
    results = []
    for tag in tree.xpath("//a[contains(text(), '{}') and @class='js-navigation-open link-gray-dark']".format(query.lower())):
        res = {}
        res['type'] = 'Aiogram example'
        res['title'] = tag.xpath('text()')[0]
        res['link'] = '{}{}'.format(
            'https://github.com', tag.xpath('@href')[0])
        results.append(res)

    return results if results else None
