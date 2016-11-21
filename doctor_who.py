import requests
from bs4 import BeautifulSoup
import pandas as pd


# Pull pages for each episode
url = 'http://www.chakoteya.net/DoctorWho/episodes1.htm'
result = requests.get(url)
content = result.content

soup = BeautifulSoup(content, 'lxml')  # Parse the HTML as a string
html_table = soup.find_all('table')[0]  # Grab the first table
episodes = pd.DataFrame(columns=['Episode','Production','Airdate'])

for row in html_table.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) == 3:
        episodes = episodes.append({'Episode':cells[0].text,
                                    'Production':cells[1].text,
                                    'Airdate':cells[2].text.replace('\r\n', ' ')
                                    },
                                   ignore_index=True)

episodes = episodes.ix[3:]
print episodes
