import requests
from bs4 import BeautifulSoup
import urllib3

def forum_spider(max_pages):
    page = 1
    while page <= max_pages:
        url = 'https://forums.triplea-game.org/category/45/play-by-forum?lang=en-US&page=' + str(page)
        source_code = requests.get(url)
        plain_text_code = source_code.text
        # need to convert to a bs4 object
        soup = BeautifulSoup(plain_text_code, features="html.parser")

        for link in soup.findAll('a', {'itemprop' : 'url'}):
            # 'a' stands for anchor in html. finds all links with itemprop
            title = link.string
            href = 'https://forums.triplea-game.org' + link.get('href')
            print(title)
            print(href)
            save_finder(href, 1)
            print("\r")

        page += 1

def save_finder(item_url, max_pages):
    page = 1
    while page <= max_pages:
        url = item_url + '/36?lang=en-US&page=' + str(page)
        source_code = requests.get(url)
        plain_text_code = source_code.text
        soup = BeautifulSoup(plain_text_code, features="html.parser")

        page += 1

# > Savegame < / a > < / p >

forum_spider(2)
