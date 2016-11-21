import requests
from urlparse import urljoin
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd


# Pull pages for each episode
url = 'http://www.chakoteya.net/DoctorWho/episodes1.htm'
result = requests.get(url)
content = result.content

soup = BeautifulSoup(content, 'lxml')  # Parse the HTML as a string
html_table = soup.find_all('table')[0]  # Grab the first table
episodes = pd.DataFrame(columns=['Episode', 'Link', 'Production', 'Airdate'])

for row in html_table.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) ==3 and cells[0].find(href=True):
        Episode = cells[0].text
        Link = urljoin(url, cells[0].find(href=True)['href'])
        Production = cells[1].text
        Airdate = cells[2].text.replace('\r\n', ' ')
        episodes = episodes.append({'Episode': Episode,
                                    'Link': Link,
                                    'Production': Production,
                                    'Airdate': Airdate
                                     },
                                     ignore_index=True)

# episodes = episodes.ix[3:]
print episodes
