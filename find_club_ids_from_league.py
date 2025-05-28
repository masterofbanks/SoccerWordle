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
 
list = ["https://fbref.com/en/squads/822bd0ba/Liverpool-Stats", "https://fbref.com/en/squads/18bb7c10/Arsenal-Stats", "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats", "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats", "https://fbref.com/en/squads/19538871/Manchester-United-Stats", "https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats", "https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats", "https://fbref.com/en/squads/8602292d/Aston-Villa-Stats", "https://fbref.com/en/squads/d48ad4ff/Napoli-Stats", "https://fbref.com/en/squads/d609edc0/Internazionale-Stats", "https://fbref.com/en/squads/e0652b02/Juventus-Stats", "https://fbref.com/en/squads/dc56fe14/Milan-Stats", "https://fbref.com/en/squads/cf74a709/Roma-Stats", "https://fbref.com/en/squads/206d90db/Barcelona-Stats", "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats", "https://fbref.com/en/squads/db3b9613/Atletico-Madrid-Stats", "https://fbref.com/en/squads/e2d8892c/Paris-Saint-Germain-Stats", "https://fbref.com/en/squads/054efa67/Bayern-Munich-Stats", "https://fbref.com/en/squads/c7a9f859/Bayer-Leverkusen-Stats", "https://fbref.com/en/squads/add600ae/Dortmund-Stats"]
otherlist = []
for x in list:
    otherlist.append(x[28:36])
answer = "" 
for thing in otherlist:
    answer += ("current_club = \\\'" + thing + "\\\' OR ")
print(answer)