from .models import Task, Page
from django.utils import timezone
from django.conf import settings
from queue import Queue
from datetime import timedelta
from bs4 import BeautifulSoup
from bs4.element import Comment
from celery import shared_task

import logging
import requests
import os
import re

logger = logging.getLogger('crawler')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(filename=settings.CRAWLER_LOG_FILE)
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def is_url_valid(url):
    try:
        res = requests.head(url)
        is_status_valid = res.status_code == 200
        is_header_valid = False
        possible_headers = ['content-type', 'Content-Type', 'Content-type', 'CONTENT-TYPE']
        for header in possible_headers:
            if header in res.headers.keys():
                is_header_valid = res.headers[header].startswith('text/html')
        return is_status_valid and is_header_valid
    except Exception as ex:
        return False

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def get_text_from_soup(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)


def crawl_data(url, levels, token_file):

    process_queue = Queue()
    process_queue.put({'level':0, 'url':url})

    while process_queue.empty() == False:

        data = process_queue.get()
        level = data['level']
        url = data['url']
        page = None
        urls = []
        text = None
        need_to_crawl = True

        if Page.objects.filter(url=url).count() > 0:
            page = Page.objects.filter(url=url).first()
            delta = timezone.now()-page.last_updated_at
            if delta.days <= 3:
                text = page.text
                urls = page.urls
                need_to_crawl = False
        
        logger.info(f'level:::{level} url:::{url} need_to_crawl:::{need_to_crawl}')

        if need_to_crawl == True:
            html_content = requests.get(url).content
            soup = BeautifulSoup(html_content, 'html.parser')
            text = get_text_from_soup(soup)
            links = soup.findAll('a')

            for link in links:
                try:
                    if link['href'].startswith('http') and is_url_valid(url) == True:
                            urls.append(link['href'])
                    elif link['href'].startswith('/'):
                        temp_url = url+link['href']
                        if is_url_valid(temp_url) == True:
                            urls.append(temp_url)

                except Exception as ex:
                    logger.error(f'level:::{level} url:::{url} error while processing links::{ex}')



        logger.info(f'level:::{level} url:::{url} processed webpage')
        token_file.writelines(text) 
        
        if level+1 < levels:
            for url in urls:
                if is_url_valid(url):
                    logger.info(f'level:::{level+1} url:::{url} added url')
                    process_queue.put({'level':level+1, 'url':url})

        if page is None:
            page = Page.objects.create(url=url, text=text, urls=urls, last_updated_at=timezone.now())
        elif need_to_crawl == True:
            page.text = text
            page.urls = urls
            page.last_updated_at = timezone.now()
            page.save()

def digest_token_file(token_file):
    logger.info(f'digesting tokens')
    lines = token_file.readlines()
    freq_data = {}
    for line in lines:
        words = lines.split()
        for word in words:
            if word not in stop_words:
                if word in freq_data.keys():
                    freq_data[word] = freq_data[word]+1
                else :
                    freq_data[word] = 1
    logger.info(f'done with token digestion')
    return freq_data


@shared_task
def start_processing(task_id):
    
    task = Task.objects.filter(id=task_id).first()
    token_file = open(os.path.join(settings.DATA_DUMP, f'{task_id}.txt'), 'w')
    task.status = 'i'
    task.save()
    crawl_data(task.url, task.level, token_file)
    freq_data = digest_token_file(token_file)
    token_file.close()
    task.freq_data = freq_data
    task.finished_at = timezone.now()
    task.status = 'c'
    task.save()
