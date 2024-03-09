import asyncio
import time
from math import ceil
from pprint import pprint

import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from furl import furl
from selenium import webdriver


def kwork_parser(categories='', tasks_count=1):
    tasks = []
    pages_count = ceil(tasks_count / 12)

    for page in range(1, pages_count + 1):
        tasks.extend(
            parse_kwork_freelance_page('', page)
        )

    return tasks[:tasks_count]


def parse_kwork_freelance_page(categories, page):
    url = furl("https://kwork.ru/projects?fc=41")
    url.args['page'] = page

    op = webdriver.ChromeOptions()
    op.add_argument('headless')

    result_tasks = []

    driver = webdriver.Chrome(options=op)
    driver.get(url.url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    tasks = soup.select('.want-card')

    result_tasks.extend(
        dict(
            title=task.select_one('.wants-card__header-title').a.text.replace('\n', '').strip(),
            resp_count=int(task.select('.query-item__info span')[1].text.split(' ')[1]),
            url='https://kwork.ru'
                + task.select_one('.wants-card__header-title').a.get('href'),
        )
        for task in tasks
    )
    return result_tasks