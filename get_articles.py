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
    expr = "//a[contains(@href, $query) and @class='anchor']"
    results = []

    async with aiohttp.ClientSession() as session:
        content = await fetch(session, url)

    try:
        tree = html.fromstring(content)
    except:
        return []

    for tag in tree.xpath(expr, query=query.lower()):
        res = {
            'type': 'API Reference',
            'title': tag.xpath('following-sibling::text()')[0],
            'link': '{}{}'.format(url, tag.xpath('@href')[0])
        }
        results.append(res)

    return results


async def get_aiogram_examples(query: str):
    url = 'https://github.com/aiogram/aiogram/tree/dev-2.x/examples'
    expr = "//a[contains(text(), $query) and @class=$tag_class]"
    tag_class = 'js-navigation-open link-gray-dark'
    results = []
    async with aiohttp.ClientSession() as session:
        content = await fetch(session, url)

    try:
        tree = html.fromstring(content)
    except:
        return []

    for tag in tree.xpath(expr, query=query.lower(), tag_class=tag_class):
        res = {
            'type': 'Aiogram example',
            'title': tag.xpath('text()')[0],
            'link': '{}{}'.format('https://github.com', tag.xpath('@href')[0])
        }
        results.append(res)

    return results
