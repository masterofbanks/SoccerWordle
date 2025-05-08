import requests
from bs4 import BeautifulSoup
import time
import unidecode
from datetime import date
from unidecode import unidecode
 
def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
 
    return age

#open files
clubFile = open("allclubs.csv", "w")
firstClubLine = "id,name\n"
clubFile.write(firstClubLine)
playerFile = open("allplayers.csv", "w")
firstPlayerLine = "id,name,positions,foot,height,age,nationality,current_club,gls,assists,mp,cpf\n"
playerFile.write(firstPlayerLine)


# Making a GET requests

top_url = 'https://fbref.com/'
leauges = ['https://fbref.com/en/comps/12/La-Liga-Stats','https://fbref.com/en/comps/9/Premier-League-Stats', 'https://fbref.com/en/comps/11/Serie-A-Stats', 'https://fbref.com/en/comps/20/Bundesliga-Stats', 'https://fbref.com/en/comps/13/Ligue-1-Stats']
r = requests.get('https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats') 
print(r.ok)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')


s = soup.find('table', id = 'big5_table') 
subMenu = s.find('tbody')
clubs = subMenu.find_all('tr')
print(len(clubs))