from bs4 import BeautifulSoup

import requests

url = "http://flightaware.com/live/airport/KDFW/departures/airline"

page = requests.get(url)

data = page.content

soup = BeautifulSoup(data, "html.parser")

#get all the tables
tables = soup.find_all('table', class_='prettyTable')

for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        data = row.find_all('td')
        for datum in data:
            s = datum.text;
            s = s.strip()
            print(s)
        print('############### NEW ROW ###############')
