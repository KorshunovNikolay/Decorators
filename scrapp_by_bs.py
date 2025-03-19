import requests
import bs4
import re
from datetime import datetime

from with_params import logger

start = datetime.now()
path = 'bs.log'

# Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Формируем soup
def get_soup(link):
    response = requests.get(link)
    soup = bs4.BeautifulSoup(response.text, features='lxml')
    return soup

# Избавляемся от знаков препинаний
def clean(text:str):
    clean_text = re.sub(r"[^\w\s]", ' ', text)
    return clean_text

# Получаем ссылки на статьи
@logger(path)
def get_article_link_list():
    article_link_list = []
    articles_list = get_soup('https://habr.com/ru/articles/').find_all(name='h2', class_=['tm-title'])
    for article in articles_list:
        article_link = 'https://habr.com' + article.find(name='a', class_='tm-title__link')['href']
        article_link_list.append(article_link)
    return article_link_list

# Получаем текст статьи
@logger(path)
def get_article_text(link:str):
    raw_text = get_soup(link).find(name='div', attrs={'xmlns': 'http://www.w3.org/1999/xhtml'})
    text = raw_text.get_text(separator=' ')
    return text

# Получаем заголовок статьи
@logger(path)
def get_title(link:str):
    title = get_soup(link).find(name='h1', attrs={'data-test-id': 'articleTitle'}).text
    return title

# Получаем время размещения статьи
@logger(path)
def get_time(link:str):
    time = get_soup(link).find(name='span', class_='tm-article-datetime-published')
    return time.find('time')['datetime']

# Поиск статей по заданным словам
def article_search_by_words(words_list:list, articles_list:list):
    for article_link in articles_list:
        time = get_time(article_link)
        title = get_title(article_link)
        text = get_article_text(article_link)
        words_in_text = clean(text.lower()).split()
        words_in_title = clean(title.lower()).split()
        found_words = set(words_list) & (set(words_in_text) | set(words_in_title))
        if found_words:
            print(f"{time[:-5]} - {title} - {article_link}. "
                  f"Совпадения: {', '.join(found_words)}.")

if __name__ == '__main__':
    links = get_article_link_list()
    article_search_by_words(KEYWORDS, links)

finish = datetime.now()
print(f"Время выполнения программы: {finish - start}")