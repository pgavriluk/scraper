import requests
import pprint
from bs4 import BeautifulSoup

url = 'https://news.ycombinator.com/'
response_main_page = requests.get(url)
response_page_2 = requests.get(url + 'news?p=2')

soup = BeautifulSoup(response_main_page.text + response_page_2.text, 'html.parser')

story_links = soup.select('.storylink')
subtext_elements = soup.select('.subtext')


def sort_stories_by_votes(stories):
    return sorted(stories, key=lambda k: k['score'], reverse=True)


def create_custom_stories(links, subtexts):
    stories = []
    for index, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtexts[index].select('.score')
        if len(vote):
            score = int(vote[0].getText().replace(' points', ''))
            if score > 100:
                if not href.startswith('http'):
                    href = url + href
                stories.append({'title': title, 'link': href, 'score': score})

    return sort_stories_by_votes(stories)


def get_news():
    return create_custom_stories(story_links, subtext_elements)

pprint.pprint(get_news())