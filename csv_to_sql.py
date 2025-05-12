
def replace_apost(s):
    result = ""
    for letter in s:
        if letter == '\'':
            result += "\'\'"
        else:
            result += letter
    return result




def break_csv_line(l):
    words = []
    x = 0
    start = 0

    for letter in l:
        if letter == ",":
            word = replace_apost(l[start:x])
            word = '\'' +  word + '\''
            words.append(word)
            start = x + 1

        x += 1
    word = '\'' + l[start:x-1] + '\''
    words.append(word)
    return words


player_csv = open('goodData/allPlayers.csv', 'r')
next(player_csv)


club_csv = open('goodData/allClubs.csv', 'r')
next(club_csv)


if(player_csv.closed):
    print("Player csv file is closed")


if(club_csv.closed):
    print("Club csv file is closed")


sql_file = open('clubs_and_players.sql', "w")

create_player_table = """create table player (
    player_id VARCHAR(8) NOT NULL PRIMARY KEY,
    player_name VARCHAR(150) NOT NULL,
    positions VARCHAR(150) NOT NULL,
    foot VARCHAR(150),
    height int,
    age int,
    nationality VARCHAR(50),
    current_club VARCHAR(8),
    goals int NOT NULL,
    assists int NOT NULL,
    matches_played int NOT NULL,
    clubs_played_for VARCHAR(400) NOT NULL
);
"""

sql_file.write(create_player_table)

create_club_table = """create table club (
    club_id VARCHAR(8) NOT NULL PRIMARY KEY,
    club_name VARCHAR(250) NOT NULL
);
"""
sql_file.write(create_club_table)
#test = "08f5afaa,Gianluigi Donnarumma,GK,Right,196,26,Italy,e2d8892c,0,0,37,dc56fe14 e2d8892c"


for line in player_csv:
    new_sql_line = "insert into player (player_id, player_name, positions, foot, height, age, nationality, current_club, goals, assists, matches_played, clubs_played_for) values ("
    attributes = break_csv_line(line)
    for a in attributes:    
        if(a == "\'None\'"):
            new_sql_line += "null, "
        else:
            new_sql_line += (a + ", ")
        
    new_sql_line = new_sql_line[:len(new_sql_line)- 2] + ");\n"
    sql_file.write(new_sql_line)



for line in club_csv:
    new_sql_line = "insert into club (club_id, club_name) values ("
    attributes = break_csv_line(line)
    for a in attributes:    
        if(a == "\'None\'"):
            new_sql_line += "null, "
        else:
            new_sql_line += (a + ", ")
        
    new_sql_line = new_sql_line[:len(new_sql_line)- 2] + ");\n"
    sql_file.write(new_sql_line)








