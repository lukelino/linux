import os
import re
import requests
from collections import deque
from colorama import Fore, Style, init

from bs4 import BeautifulSoup

viewed_pages = deque()
path = r'/home/lukasz/Py/122_Text_Browser/dir-for-webs'
os.makedirs(path, exist_ok=True)


def create_filename(user_url):
    pattern = re.compile(r'^(\w*\:\/\/)|(\.\w{2,3})$')  # finds http:// https:// and .com
    file_name = re.sub(pattern, '', user_url)
    return file_name


def add_to_viewed_pages(link):
    if not viewed_pages:
        viewed_pages.appendleft(link)
    else:
        if viewed_pages[0] != link:
            viewed_pages.appendleft(link)


def run_url(previous_page):
    with open(os.path.join(path, previous_page)) as file:
        previous_page_text = file.readlines()
        for elem in previous_page_text:
            print(elem.strip())
    add_to_viewed_pages(previous_page)


def get_soup(user_url):
    init(autoreset=True)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    response = requests.get(user_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    page = ''
    for tag in soup.find_all(['title', 'p', re.compile('^h'), 'a', 'ul', 'ol', 'li', 'span'], text=True):
        if tag.name == 'a':
            page += Fore.BLUE + tag.text + '\033[39m' + ' '
        else:
            page += tag.text + '\n'
    formatted_text = re.sub('\n+', '\n', page)
    formatted_text = re.sub('\s{2,}', '\n', formatted_text)
    # final_page_text = re.sub('s+', '', formatted_soup)
    return formatted_text


def save_the_new_site_to_file(file_n, page_text):
    with open(os.path.join(path, file_n), 'w', encoding='utf-8') as file:
        file.write(page_text)


while (url := input()) != 'exit':
    f_name = create_filename(url)

    if url == 'back':
        if len(viewed_pages) > 1:
            current = viewed_pages.popleft()
            previous = viewed_pages.popleft()
            print(previous)
            run_url(previous)
        else:
            continue

    elif not os.path.exists(os.path.join(path, f_name)):
        if not url.startswith('https://'):
            url = 'https://' + url

        try:
            txt_page = get_soup(url)
        except Exception as err:
            print('Page not found', err)
            continue
        if txt_page:
            print(txt_page)
            save_the_new_site_to_file(f_name, txt_page)
            add_to_viewed_pages(f_name)
        else:
            continue

    elif os.path.exists(os.path.join(path, f_name)):
        run_url(f_name)
