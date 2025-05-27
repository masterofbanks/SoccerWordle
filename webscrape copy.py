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
def cheat(input):
    answer = ""
    match input:
        case "822bd0ba"| "18bb7c10"| "b8fd03ef"| "cff3d9bb"| "b2b47a98"| "8602292d"| "e4a775cb"| "d07537b9"| "4ba7cbea"| "cd051869"| "fd962109"| "47c64c55"| "d3fd31cc"| "7c21e445"| "19538871"| "8cec06e1"| "361ca564"| "a2d435b3"| "b74092de"| "33c895d4" :
            return "Premier League"
        case "206d90db"| "53a2f082"| "db3b9613"| "2b390eca"| "2a8183b3"| "fc536746"| "f25da7fb"| "f25da7fb"| "03c57e2b"| "2aa12281"| "e31d1cd9"| "dcc91a7b"| "7848bd64"| "a8661628"| "8d6fd021"| "9024a00a"| "ad2be733"| "7c6f2c78"| "0049d422"| "17859612":
            return "La Liga"
        case "054efa67"| "c7a9f859"| "f0ac8ee6"| "add600ae"| "a486e511"| "a224b06a"| "acbb6a5b"| "62add3bf"| "598bc722"| "32f3ee20"| "4eaa11d7"| "0cdc4311"| "7a41008f"| "54864664"| "033ea6b8"| "18d9d2a7"| "2ac661d9"| "b42c6323":
            return "Bundesliga"
        case "d48ad4ff"| "d609edc0"| "922493f3"| "e0652b02"| "cf74a709"| "421387cf"| "7213da33"| "dc56fe14"| "1d8099f8"| "28c9c3cd"| "105360fe"| "04eea015"| "658bf2de"| "0e72edf2"| "c4260e09"| "eab4234c"| "ffcbe334"| "a3d88bd8"| "af5d5982"| "21680aa4":
            return "Serie A"
        case "e2d8892c"| "5725cc7b"| "fd6114db"| "132ebc33"| "cb188c0c"| "d53c0b06"| "c0d3eab4"| "fd4e0f7d"| "fb08dbb3"| "3f8c4b5f"| "5ae09109"| "b3072e00"| "d7a486cd"| "69236f98"| "5c2737db"| "7fdd64e0"| "d298ef2c"| "281b0e73":
            return "Ligue 1"
        case _: return "None"
    return "None"





#open files
clubFile = open("bruhclubs.csv", "w")
firstClubLine = "id,name\n"
clubFile.write(firstClubLine)
playerFile = open("bruhplayers.csv", "w")
firstPlayerLine = "id,name,positions,foot,height,age,nationality,current_club,gls,assists,mp,league\n"
playerFile.write(firstPlayerLine)


# Making a GET requests

top_url = 'https://fbref.com/'

player_url = "https://fbref.com/en/players/0b8c9180/Aron-Yaakobishvili"







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
                    c = cheat(currentClub)
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




playerLine += c
playerLine += '\n'
print(playerLine)
playerFile.write(playerLine)