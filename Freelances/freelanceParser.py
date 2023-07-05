from itertools import chain
from math import ceil

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from furl import furl
import asyncio
import aiohttp


async def freelance_parser(categories='', tasks_count=1):
    async_tasks = []

    pages = ceil(tasks_count / 25)
    async with aiohttp.ClientSession() as session:
        async_tasks.extend(
            parse_freelance_tasks_page(session, categories, page)
            for page in range(1, pages + 1)
        )
        tasks = await asyncio.gather(*async_tasks)
        all_tasks = list(chain.from_iterable(tasks))
        return all_tasks[:tasks_count]


async def parse_freelance_tasks_page(session, categories='', page=1):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    url = furl('https://freelance.ru/project/search/pro?c=&q=&m=&e=&a=&a=&v=&f=&t=&o=&o=&b=')
    url.args['page'] = page

    result_tasks = []

    async with session.get(url.url, headers=headers) as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        tasks = soup.select('.project')
        result_tasks.extend(
            dict(
                title=task.select_one('.title').a.text.replace('\n', '').strip(),
                resp_count=int(task.select_one('.comments-count').text)
                if task.select_one('.comments-count')
                else 0,
                time_ago=task.select_one('.timeago').text.strip(),
                url='https://freelance.ru'
                + task.select_one('.title').a.get('href'),
            )
            for task in tasks
            if not task.select_one('.up')
        )
    return result_tasks
