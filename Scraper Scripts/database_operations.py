import pyodbc


def load_data(df):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-OQUP3K1;'
                          'Database=metacritic;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    # load into game_props
    if df['UserScore'][0] is None:
        cursor.execute('INSERT INTO dbo.game_props([GameName], [Platform], [ReleaseDate])'
                       'VALUES (?,?,?)', df['GameName'][0], df['Platform'][0], df['ReleaseDate'][0])
        cursor.execute('INSERT INTO dbo.scoring([UserScore], [CriticScore])'
                       'VALUES (?,?)',  None, float(df['CriticScore'][0]))
    else:
        cursor.execute('INSERT INTO dbo.game_props([GameName], [Platform], [ReleaseDate])'
                            'VALUES (?,?,?)',  df['GameName'][0], df['Platform'][0], df['ReleaseDate'][0])
        cursor.execute('INSERT INTO dbo.scoring([UserScore], [CriticScore])' 
                            'VALUES (?,?)',  df['UserScore'][0], float(df['CriticScore'][0]))
    conn.commit()



# returns true if the game is in the database else false

def check_game_loaded(game_name, release_date):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-OQUP3K1;'
                          'Database=metacritic;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    cursor.execute("SELECT ScoringID "
                   "FROM dbo.game_props "
                   "WHERE GameName = \'" + game_name + "\'"
                   "AND ReleaseDate = \'" + str(release_date) + "\'")
    result = cursor.fetchone()
    result = None if result is None else result[0]
    return result


def update_data(df, score_id):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-OQUP3K1;'
                          'Database=metacritic;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    # load into game_props
    if df['UserScore'][0] is None:
        cursor.execute("UPDATE dbo.scoring "
                       "SET UserScore = Null ,CriticScore = {0}".format(df['CriticScore'][0]) +
                       "WHERE ScoringID = {0}".format(score_id))
    else:
        cursor.execute("UPDATE dbo.scoring "
                   "SET UserScore = {:.1f}".format(df['UserScore'][0]) +
                    ",CriticScore = {0}".format(df['CriticScore'][0]) +
                   "WHERE ScoringID = {0}".format(score_id))
    conn.commit()


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default



