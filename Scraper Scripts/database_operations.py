import pyodbc


def load_data(df):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-OQUP3K1;'
                          'Database=metacritic;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    # load into game_props
    if df['UserScore'][0] is None:
        cursor.execute('INSERT INTO dbo.game_props([GameID], [GameName], [Platform], [ReleaseDate])'
                       'VALUES (?,?,?,?)', float(df['GameID'][0]), df['GameName'][0], df['Platform'][0], df['ReleaseDate'][0])
        cursor.execute('INSERT INTO dbo.scoring([GameID], [UserScore], [CriticScore])'
                       'VALUES (?,?,?)', float(df['GameID'][0]), None,
                       float(df['CriticScore'][0]))
    else:
        cursor.execute('INSERT INTO dbo.game_props([GameID], [GameName], [Platform], [ReleaseDate])'
                            'VALUES (?,?,?,?)',  float(df['GameID'][0]), df['GameName'][0], df['Platform'][0], df['ReleaseDate'][0])
        cursor.execute('INSERT INTO dbo.scoring([GameID], [UserScore], [CriticScore])' 
                            'VALUES (?,?,?)', float(df['GameID'][0]), df['UserScore'][0], float(df['CriticScore'][0]))
    conn.commit()


# returns -1 if no game is loaded with that name, else returns the ID for that game
# only works if game names are strictly identical

def check_game_loaded(game_name):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-OQUP3K1;'
                          'Database=metacritic;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    cursor.execute("SELECT GameID "
                   "FROM dbo.game_props "
                   "WHERE GameName = \'" + game_name + "\'")
    result = cursor.fetchone()
    result = -1 if result is None else result[0]
    return result

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default



