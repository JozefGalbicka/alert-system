from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
import requests
import os
import re
import logging

script_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


# return list of articles, each article is represented as html code
def get_articles():
    source = requests.get('https://www.iklub.sk/').text
    soup = BeautifulSoup(source, 'lxml')

    table = soup.find('table', class_='blog').tr.td

    regex_articles = re.compile('oznam\d\d\d\d$')

    articles = table.find_all('div', {'id': regex_articles})
    return articles


def get_last_article_title():
    articles = get_articles()

    regex_content = re.compile('oznam\d\d\d\d')
    # extract first html line of first article and find title (div id = oznam\d\d\d\d)
    return str(regex_content.findall((str(articles[0])).splitlines()[0])[0])


def get_new_articles():
    with open('config/lastarticle.txt', 'r') as f:
        last_article = f.readline().strip()

    articles = get_articles()
    new_articles = []

    for article in articles:
        # extract first html line of article and find id of article (div id = oznam\d\d\d\d)
        regex_content = re.compile('oznam\d\d\d\d')
        match = regex_content.findall((str(article)).splitlines()[0])[0]

        # when found article is article which was already sent last time, break cycle
        if match == last_article:
            break

        # text content
        title = article.table.tr.td.a.text.strip()
        subtitle = article.find('div', {'id': match + "podnadpis"}).text
        text = (article.find('div', {'id': match + "text"}).text.strip())

        # text section of article in html
        textHTML = article.find('div', {'id': match + "text"})
        # url section of text section in html
        urlsHTML = textHTML.find_all('a', href=True)

        # getting all url names and links
        urls = dict()
        for url in urlsHTML:
            urls[url.text.strip()] = url['href']
            text = text.replace(url.text.strip(), '')

        new_articles.append(Article(title, subtitle, text, urls))

    if new_articles:
        with open('config/lastarticle.txt', 'w') as f:
            f.write(get_last_article_title())
            logger.info(f"lastarticle.txt was successfully updated.")
        logger.info(f"Found {len(new_articles)} new articles on iklub.sk")
    else:
        logger.info(f"No new articles found on iklub.sk.")

    # reversing, so oldest articles will be on start of our list
    new_articles.reverse()
    return new_articles


class Article:
    def __init__(self, title, subtitle, text, urls):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.urls = urls


