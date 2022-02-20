import sqlite3

COLUMNS = 7
ROWS = 6

def CreatePlayerTable():
    conn = sqlite3.connect('Databases.db')
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS player(PLAYER TEXT PRIMARY KEY,ELO_SCORE REAL,TOT_GAMES INTEGER,WINNINGS INTEGER,LOSSES INTEGER,TIES INTEGER)")

    conn.commit()
    conn.close()

def CreateLoadVariables():
    conn = sqlite3.connect('Databases.db')
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS loadvariables(COLOUR1 TEXT,COLOUR2 TEXT,Player1 TEXT, Player2 TEXT,PLAYER INTEGER)")
    conn.commit()
    cursor.execute("INSERT INTO loadvariables values ('{}','{}','{}','{}',0)".format("Yellow","Red","Player 1", "Player 2"))
    conn.commit()
    conn.close()

def CreateSaveStateTable():
    conn = sqlite3.connect('Databases.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS savestate(ROW INTEGER,COLUMN INTEGER,VALUE INTEGER)")
    conn.commit()
    cursor.execute("SELECT * FROM savestate ")
    l = cursor.fetchall()
    conn.commit()
    if len(l) == 0:
        for i in range(ROWS):
            for j in range(COLUMNS):
                cursor.execute("INSERT INTO savestate values({},{},{})".format(j, i, 0))
                conn.commit()
    conn.close()


def CreateTheTables():
    CreatePlayerTable()
    CreateSaveStateTable()
    CreateLoadVariables()