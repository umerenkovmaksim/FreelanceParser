from itertools import chain
from math import ceil

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from furl import furl
import asyncio
import aiohttp


async def habr_parser(categories='', tasks_count=1):
    async_tasks = []

    pages = ceil(tasks_count / 25)
    async with aiohttp.ClientSession() as session:
        async_tasks.extend(
            parse_habr_tasks_page(session, categories, page)
            for page in range(1, pages + 1)
        )
        tasks = await asyncio.gather(*async_tasks)
        all_tasks = list(chain.from_iterable(tasks))
        return all_tasks[:tasks_count]


async def parse_habr_tasks_page(session, categories='', page=1):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    url = furl('https://freelance.habr.com/tasks')
    url.args['categories'] = categories.replace(' ', '')
    url.args['page'] = page

    result_tasks = []

    async with session.get(url.url, headers=headers) as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        tasks = soup.select('.content-list__item')
        result_tasks.extend(
            dict(
                title=task.a.text,
                resp_count=int(task.select_one('.params__responses').i.text)
                if task.select_one('.params__responses')
                else 0,
                time_ago=task.select_one('.params__published-at').text.strip(),
                url='https://freelance.habr.com' + task.a.get('href'),
            )
            for task in tasks
        )
    return result_tasks
