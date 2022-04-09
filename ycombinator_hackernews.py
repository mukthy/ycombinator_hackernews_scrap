import requests
from bs4 import BeautifulSoup
import pprint


def sort_hn_by_votes(hn):
    return sorted(hn, key=lambda x: x['votes'], reverse=True)


def hn_scrape(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            # print(points)
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})

    return sort_hn_by_votes(hn)


count = 1

while True:
    try:
        url = f'https://news.ycombinator.com/news?p={count}'
        response = requests.get(f'{url}')
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.titlelink')
        subtext = soup.select('.subtext')
        next_page = soup.select('.morelink')[0].get('href')
        print(url)
        pprint.pprint(hn_scrape(links, subtext))
        count = count + 1

    except IndexError:
        print('Completed! No More Pages')
        break
