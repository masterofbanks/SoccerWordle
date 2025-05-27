import requests
from bs4 import BeautifulSoup
import time
import unidecode
from datetime import date
from unidecode import unidecode

#things to implement
# 1. add clubs from cpf into the clubs database
# 2. setup postgresql database, maybe with neon,; use sql tools in vs code and python
# 3. start making queries
# 4. get images of players
# 5. get images of clubs (perhaps manually)
# 
# 
# 
# #
 
def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
 
    return age

def getClubName(href):
    ns = 0
    i = 0
    numSlashes = href.count('/')
    if(numSlashes > 5):
        while(ns < numSlashes):
            if(href[i] == '/'):
                ns += 1
            i+=1
    #print(href[i:href.find('Stats')-1])
    return href[i:href.find('Stats')-1]

#open files
clubFile = open("allClubs.csv", "w")
firstClubLine = "id,name\n"
clubFile.write(firstClubLine)
playerFile = open("allPlayers.csv", "w")
firstPlayerLine = "id,name,positions,foot,height,age,nationality,current_club,gls,assists,mp,cpf\n"
playerFile.write(firstPlayerLine)


# Making a GET requests

top_url = 'https://fbref.com/'
time.sleep(5)

r = requests.get('https://fbref.com/en/comps/13/Ligue-1-Stats') 
print(r.ok)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

s = soup.find('table', id = 'results2024-2025131_overall') 
subMenu = s.find('tbody')
clubs = subMenu.find_all('tr')
x = 0
list = []
#navigate to a club by getting its url
for td in clubs:
    a = td.find('a')
    newEnding = a.get('href')
    id = newEnding[11:19]
    list.append(id)
answer = ""
for thing in list:
    answer += ('\"' + thing + '\"' + ", ")

print(answer)
