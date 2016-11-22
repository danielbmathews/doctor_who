import requests
from urlparse import urljoin
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import time


def get_episodes_info(season_url):

    print 'checking {}'.format(season_url)

    # Set up dataframe to receive information
    episodes = pd.DataFrame(
        columns=['Episode', 'Link', 'Production', 'Airdate'])

    # Pull html table from the page
    content = requests.get(season_url).content
    soup = BeautifulSoup(content, 'lxml')  # Parse HTML as a string
    html_table = soup.find_all('table')[0]  # Get first table

    # Iterate through the rows of the html table
    for row in html_table.find_all("tr"):
        cells = row.find_all("td")

        # Limit down to rows that give info about an episode
        if len(cells) ==3 and cells[0].find(href=True):
            Episode = cells[0].text
            Link = urljoin(season_url, cells[0].find(href=True)['href'])
            Production = cells[1].text
            Airdate = cells[2].text.replace('\r\n', ' ')

            episodes = episodes.append({'Episode': Episode,
                                       'Link': Link,
                                       'Production': Production,
                                       'Airdate': Airdate},
                                       ignore_index=True)
    return episodes


def get_visible_text(url):
    # Get text
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    texts = soup.findAll(text=True)

    # Filter down to visible elements
    def _visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head',
                                   'title']:
            return False
        else:
            return True
    return ''.join(filter(_visible, texts)).strip('\r\n')


def main():
    # Set up HDFStore for storing transcripts
    store = pd.HDFStore('dw_transcripts.h5')

    # Get and store episode information
    # TODO find error for pulling data from doctors 9+
    episode_list_url = 'http://www.chakoteya.net/DoctorWho/episodes{}.htm'
    for c in range(1, 8):
        url = episode_list_url.format(c)
        print url
        key = 'Doctor_' + str(c)
        store.put(key, get_episodes_info(url))

if __name__ == '__main__':
    main()