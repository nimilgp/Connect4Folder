import sqlite3
import elo

def AddToPlayerTable(player):
    conn = sqlite3.connect('Databases.db')
    cursor = conn.cursor()
    cursor.execute("SELECT PLAYER FROM player")
    l = cursor.fetchall()
    names = [name[0] for name in l]
    conn.commit()
    if player not in names:
        # everyone starts with 1000 elo score, 0 -> tot,loss,win,tie
        cursor.execute("INSERT INTO player values('{}',100,0,0,0,0)".format(player))
        conn.commit()
    conn.close()


def ModifyPlayerTable(player1,player2,PLAYER):
    conn = sqlite3.connect('Databases.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ELO_SCORE FROM player where PLAYER = '{}'".format(player1))
    l = cursor.fetchone()
    conn.commit()
    cursor.execute("SELECT ELO_SCORE FROM player where PLAYER = '{}'".format(player2))
    m = cursor.fetchone()
    conn.commit()
    if PLAYER !=0:
        if PLAYER == 1:
            winner = player1
            loser = player2
            x = elo.rate_1vs1(l[0], m[0])
        elif PLAYER == 2:
            winner = player2
            loser = player1
            x = elo.rate_1vs1(m[0], l[0])
        cursor.execute(
            "UPDATE player SET ELO_SCORE = {} ,TOT_GAMES = TOT_GAMES + 1 ,WINNINGS = WINNINGS + 1   WHERE PLAYER = '{}'".format(
                x[0],winner))
        conn.commit()
        cursor.execute(
            "UPDATE player SET ELO_SCORE = {} ,TOT_GAMES = TOT_GAMES + 1 ,WINNINGS = WINNINGS + 1   WHERE PLAYER = '{}'".format(
                x[1], loser))
        conn.commit()
    else:
        x = elo.rate_1vs1(l[0], m[0],True)
        cursor.execute(
            "UPDATE player SET ELO_SCORE = {} ,TOT_GAMES = TOT_GAMES + 1 WHERE PLAYER = '{}'".format(
                x[0], player1))
        conn.commit()
        cursor.execute(
            "UPDATE player SET ELO_SCORE = {} ,TOT_GAMES = TOT_GAMES + 1 WHERE PLAYER = '{}'".format(
                x[1], player2))
    conn.close()


def RetrievePlayerTable(player):
    conn = sqlite3.connect('Databases.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player where PLAYER = '{}'".format(player))
    l = cursor.fetchone()
    conn.commit()
    conn.close()
    return l

def RetrieveLeaderBoard():
    conn = sqlite3.connect('Databases.db')
    cursor = conn.cursor()
    cursor.execute("SELECT player,elo_score FROM player order by elo_score desc")
    l = cursor.fetchall()
    conn.commit()
    conn.close()
    return l


def AddSaveStateTable( row, column, value):
    conn = sqlite3.connect('Databases.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE savestate SET value ={} WHERE row = {} and column ={}".format(value,row, column))
    conn.commit()
    conn.close()


def RetrieveSaveStateTable():
    conn = sqlite3.connect('Databases.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM savestate ")
    l = cursor.fetchall()
    conn.commit()
    conn.close()
    return l

def AddLoadVariables(COLOUR1,COLOUR2,Player1, Player2,PLAYER):
    conn = sqlite3.connect('Databases.db')
    cursor = conn.cursor()
    print(COLOUR1,COLOUR2,Player1, Player2,PLAYER,"********************************")
    cursor.execute("UPDATE loadvariables SET COLOUR1 ='{}',COLOUR2='{}',Player1='{}', Player2='{}',PLAYER = '{}'".format(COLOUR1,COLOUR2,Player1, Player2,PLAYER))
    conn.commit()
    conn.close()

def GetLoadVariables():
    conn = sqlite3.connect('Databases.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM loadvariables ")
    conn.commit()
    l = cursor.fetchone()
    conn.commit()
    conn.close()
    return l
