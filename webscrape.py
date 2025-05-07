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
clubFile = open("clubs.csv", "w")
firstClubLine = "id,name\n"
clubFile.write(firstClubLine)
playerFile = open("players.csv", "w")
firstPlayerLine = "id,name,positions,foot,height,age,nationality,current_club,gls,assists,mp,cpf\n"
playerFile.write(firstPlayerLine)


# Making a GET requests

top_url = 'https://fbref.com/'
r = requests.get('https://fbref.com/en/comps/9/Premier-League-Stats') #https://fbref.com/en/comps/9/Premier-League-Stats
print(r.ok)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')


s = soup.find('table', id = 'results2024-202591_overall') 
subMenu = s.find('tbody')
clubs = subMenu.find_all('tr')
x = 0

#navigate to a club by getting its url
for td in clubs:
    a = td.find('a')
    newEnding = a.get('href')
    id = newEnding[11:19]
    name = a.text
    name = unidecode(name)
    new_url = top_url + newEnding[1:]

    clubLine = id + "," + name +'\n'
    clubFile.write(clubLine)

    # #navigate to club's website

    print(new_url)
    time.sleep(5)
    newRequest = requests.get(new_url)
    print(newRequest.ok)
    newSoup = BeautifulSoup(newRequest.content, 'html.parser')

    #navigate to the all competitions version 
    allComps = newSoup.find('div', id = 'content').find('a').get('href')
    allCompsUrl = top_url + allComps[1:]

    time.sleep(5)

    print(allCompsUrl)
    newRequest = requests.get(allCompsUrl)
    print(newRequest.ok)
    newSoup = BeautifulSoup(newRequest.content, 'html.parser')


    #navigate to the list of players
    tableOfPlayers = newSoup.find('div', id = 'all_stats_standard')

    subMenu = newSoup.find('tbody')
    players = subMenu.find_all('tr')

    # vanDijk_info = players[0]
    # vanDijk_url = vanDijk_info.find('a').get('href')
    # vanDijk_url = top_url + vanDijk_url[1:]


    # time.sleep(5)
    for player in players:
        player_url = player.find('a').get('href')
        player_url = top_url + player_url[1:]
        time.sleep(5)


        ####################


        
        playerLine = ""
        newRequest = requests.get(player_url)
        print(newRequest.ok)
        newSoup = BeautifulSoup(newRequest.content, 'html.parser')

        playerId = player_url[29:37]
        #print(playerId)
        playerLine = playerId + ","

        playerName = newSoup.find('div', id = 'info', ).find('h1').find('span').get_text()
        playerName = unidecode(playerName)
        #print(playerName)
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
                        firstComma = playerPositions.find(',') 
                        endingParentheses = playerPositions.find(')')
                        if(firstComma == -1 and endingParentheses == -1):
                            endingDot = playerPositions.find('▪')
                            if(endingDot == -1):
                                endingDot = 10000000000
                            playerPositions = playerPositions[1:endingDot-1]
                            if(data.find('strong').next_sibling.next_sibling is not None):
                                if(data.find('strong').next_sibling.next_sibling.next_sibling is not None):
                                    foot = data.find('strong').next_sibling.next_sibling.next_sibling.string[1:]
                            #print(playerPositions)
                        else:
                            if(firstComma == -1):
                                firstComma = 1000000000000
                                    
                            startingParentheses = playerPositions.find('(') + 1
                            
                            playerPositions = playerPositions[startingParentheses:min(firstComma, endingParentheses)]
                            l = list(playerPositions)
                            i = 0
                            while( i < len(l)):
                                if(l[i] == '-'):
                                    l[i] = ' '
                                i+=1
                            playerPositions = ''.join(l)
                            #print(playerPositions)
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
            pcs = primer.find('tbody').find_all('tr')
            c = ""
            if(pcs is not None):
                set_of_clubs = set()
                for entry in pcs:
                    if(entry.find('a') is not None):
                        club_id = entry.find('a').get('href')[11:19]
                        if(club_id in set_of_clubs):
                            continue
                        else:
                            set_of_clubs.add(club_id)
                
                for i in set_of_clubs:
                    c+= (i + " ")
                c = c[:len(c)-1]
            else:
                c = currentClub

            playerLine += c
            playerLine += '\n'
            print(playerLine)
            playerFile.write(playerLine)

#print(playerLine)

#loop through the list of players
# playerNames = []
# for player in players:
#     name = player.find('th').get_text()
#     print(name)
#     playerNames.append(name)
# print(len(playerNames))

#loop through the list of clubs
#listOfTitles = []
# for club in clubs:
#     time.sleep(10)
#     td = club.find('td')
#     a = td.find('a')
#     newEnding = a.get('href')
#     withoutSlash = newEnding[1:]
#     new_url = top_url + withoutSlash
#     newRequest = requests.get(new_url)
#     print(newRequest.ok)
#     newSoup = BeautifulSoup(newRequest.content, 'html.parser')
#     top = newSoup.find('div', id = 'info')
#     subMenu = top.find('h1')
#     title = subMenu.find('span')
#     title_string = title.getText()
#     listOfTitles.append(title_string)
    

#print(listOfTitles)