import pyodbc
import pandas

def visualize():
    conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-OQUP3K1;'
                              'Database=metacritic;'
                              'Trusted_Connection=yes;')

    sql = "SELECT GameName, game_props.Platform, ReleaseDate, CriticScore, UserScore * 10 As ScaledUserScore " \
          "FROM dbo.scoring " \
          "Inner Join dbo.game_props ON scoring.ScoringID = game_props.ScoringID " \
          "WHERE YEAR(ReleaseDate) > 1995 " \
          "ORDER BY ReleaseDate ASC"

    df = pandas.io.sql.read_sql(sql, conn)
    df.groupby('ReleaseDate').ScaledUserScore.plot()

visualize()
