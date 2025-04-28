import requests
from bs4 import BeautifulSoup
import time


# Making a GET requests
top_url = 'https://fbref.com/'
r = requests.get('https://fbref.com/en/comps/9/Premier-League-Stats')
print(r.ok)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')


s = soup.find('table', id = 'results2024-202591_overall') 
#print(s)
subMenu = s.find('tbody')
clubs = subMenu.find_all('tr')
liverpool = clubs
x = 0

listOfTitles = []
for club in clubs:
    time.sleep(10)
    td = club.find('td')
    a = td.find('a')
    newEnding = a.get('href')
    withoutSlash = newEnding[1:]
    new_url = top_url + withoutSlash
    newRequest = requests.get(new_url)
    print(newRequest.ok)
    newSoup = BeautifulSoup(newRequest.content, 'html.parser')
    top = newSoup.find('div', id = 'info')
    subMenu = top.find('h1')
    title = subMenu.find('span')
    title_string = title.getText()
    listOfTitles.append(title_string)
    

print(listOfTitles)