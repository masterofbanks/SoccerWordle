import requests
from bs4 import BeautifulSoup
import time
from unidecode import unidecode

from datetime import date
 
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
clubFile = open("bruhclubs.csv", "w")
firstClubLine = "id,name\n"
clubFile.write(firstClubLine)
playerFile = open("bruhplayers.csv", "w")
firstPlayerLine = "id,name,positions,foot,height,age,nationality,current_club,gls,assists,mp,cpf\n"
playerFile.write(firstPlayerLine)


# Making a GET requests

top_url = 'https://fbref.com/'

player_url = "https://fbref.com/en/players/2eefd1b3/Andres-Cuenca"







########################################








allClubs = set()

playerLine = ""
newRequest = requests.get(player_url)
print(newRequest.ok)
newSoup = BeautifulSoup(newRequest.content, 'html.parser')

playerId = player_url[29:37]
#print(playerId)
playerLine = playerId + ","

playerName = newSoup.find('div', id = 'info', ).find('h1').find('span').get_text()
playerName = unidecode(playerName)
print(playerName)
playerLine += (playerName + ",")
#print(playerLine)
metaDeta = newSoup.find('div', id = 'meta').find_all('p')
playerPositions = ""
foot = ""
height = ""
age = ""
country = ""
currentClub = ""
for data in metaDeta:
    if(data.find('strong')):
        match data.find('strong').text:
            case "Position:":
                playerPositions = data.find('strong').next_sibling.string
                result = ""
                if(playerPositions.find('DF') != -1):
                    result += 'Defender '
                if(playerPositions.find('MF') != -1):
                    result += 'Midfielder '
                if(playerPositions.find('FW') != -1):
                    result += 'Forward '
                if(playerPositions.find('GK') != -1):
                    result += 'Goalkeeper '
                playerPositions = result[:len(result) - 1]
                print(playerPositions)
                if(data.find('strong').next_sibling.next_sibling is not None):
                    if(data.find('strong').next_sibling.next_sibling.next_sibling is not None):
                        foot = data.find('strong').next_sibling.next_sibling.next_sibling.string[1:]
                        #print(foot[1:])
            case "Born:":
                birthdate = data.find('span')['data-birth']
                year = int(birthdate[:4])
                month = int(birthdate[5:7])
                day = int(birthdate[8:10])
                #print(birthdate)
                #print(year)
                #print(month)
                #print(day)
                age = calculateAge(date(year,month,day))
                #print(age)
            case _:
                #print(data.find('strong').text)
                title = data.find('strong').text
                if(title.find("Nation") != -1 or title.find("Citizen") != -1):
                    country = data.find('a').text
                    #print(country)
                elif(title.find("Club") != -1):
                    currentClub = data.find('a').get('href')[11:19]
                    #print(currentClub)
                continue
    elif(data.find('span')):
        cm_index = data.text.find('cm')
        if(cm_index != -1):
            height = data.text[:cm_index]
            #print(height)
    
    #else:
        #print(data)

attributes = [playerPositions, foot, height, age, country, currentClub]
for x in attributes:
    if(x == ""):
        playerLine += ("None,")
    else:
        playerLine += (str(x) + ",")

#print(playerLine)
gls = 0
assists = 0
mp = 0
p1 = newSoup.find('div', {"class": "p1"})
#print(pulloutData)
if(p1 is not None):
    leagueTallies = p1.find_all('div')[2].find_all('p')
    assistTallies = p1.find_all('div')[3].find_all('p')
    matches = p1.find_all('div')[0].find_all('p')
    i = 0
    while(i < len(leagueTallies)):
        if(playerPositions != "GK"):
            gls += int(leagueTallies[i].text)
            assists += int(assistTallies[i].text)
        mp += int(matches[i].text)
        
        i+=1
    
    

playerLine += (str(gls) + ",")
playerLine += (str(assists) + ",")
playerLine += (str(mp) + ",")
#print(playerLine)
primer = newSoup.find('div', id = "all_stats_standard")
c = ""

if(primer is not None):
    if(primer.find('h2').find('span').text == ": Domestic Leagues"):
        pcs = primer.find('tbody').find_all('tr')
        if(pcs is not None):
            last_row = pcs[len(pcs) - 1]
            if(len(last_row.find_all('a')) >= 4):
                softlinks = last_row.find_all('a')
                c = softlinks[3].text
    else:
        c = "None"
        
        
else:
    c = "None"

playerLine += c
playerLine += '\n'
print(playerLine)
playerFile.write(playerLine)
a = 3000/3657 * 100
print('%.2f' % a ,'%')