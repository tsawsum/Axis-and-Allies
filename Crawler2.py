import requests
from bs4 import BeautifulSoup
import urllib3
import urllib.request
import os
import re

def forum_spider(max_pages, folder):
    page = 1
    count = 0
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
            if not save_finder(href, folder + 'Game' + str(count) + '/'):
                print('Wrong map')
            print("\r")
            count += 1

        page += 1


def save_finder(item_url, folder):
    source_code = requests.get(item_url)
    plain_text_code = source_code.text
    # Check if it's the right map
    if 'World War II v5 1942 Second Edition' in plain_text_code:
        # Find number of pages
        soup = BeautifulSoup(plain_text_code, features="html.parser")
        try:
            last_page = list(soup.findAll('li', {'class': 'page'}))[-2]
            num_pages = int(list(last_page.children)[1].string)
        except IndexError:
            # It doesn't show the total number of pages when there is only 1 page
            # which throws this exception
            num_pages = 1

        # Loop through each page
        savegame_urls = list()
        page = 1
        while page <= num_pages:
            url = item_url + '/?lang=en-US&page=' + str(page)
            source_code = requests.get(url)
            plain_text_code = source_code.text
            # Get the index of all of the savegame extensions
            savegame_idx = [m.start() for m in re.finditer('.tsvg', plain_text_code)]
            # Find the start of the url by looking for " at the start
            for idx in savegame_idx:
                i = idx
                while plain_text_code[i] != '"' and plain_text_code[i] != '>':
                    i -= 1
                if plain_text_code[i] == '"':
                    savegame_urls.append('https://forums.triplea-game.org' + plain_text_code[i+1:idx+5])
            page += 1

        # Save each file to the folder
        if not os.path.exists(folder):
            os.makedirs(folder)
        for i in range(len(savegame_urls)):
            try:
                #This does not verify on a mac because its dumb.
                urllib.request.urlretrieve(savegame_urls[i], folder + str(i) + '.tsvg')
            except:
                pass
        return True
    else:
        return False


forum_spider(2, 'Folder/To/Save/Files/In/')
