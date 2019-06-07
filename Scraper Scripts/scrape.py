from selenium import webdriver
import pandas as pd
import database_operations as db_ops
from bs4 import BeautifulSoup as soup
from datetime import datetime
import re


def main():
    # initialize variables and selenium connection
    col_names = ['GameName', 'ReleaseDate', 'Platform', 'UserScore', 'CriticScore']
    # set counter for game_id generator

    # setup driver configuration. set wait to avoid server timeouts
    chrome_path = r"C:\Users\Kevin\Desktop\scraper_stuff\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)
    driver.implicitly_wait(30)

    # for every years worth of data
    for year in range(1995, datetime.now().year + 1):
        url = "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?sort=desc&year_selected=" + \
              str(year)

        # if it hangs up, keep trying until success
        while True:
            try:
                driver.get(url)
            except:
                continue
            else:
                break

        page_soup = soup(driver.page_source, "html.parser")
        # determines how many page tags there are
        page_num_tags = len(page_soup.find_all('a', {'class': 'page_num'}))

        # if no pages element, only do one page
        if page_num_tags == 0:
            elements = page_soup.find_all('li', {'class': re.compile('product game_product*')})
            for element in elements:
                # pull GameName and Platform
                game_name_and_platform = element.div.div.a.text
                splitter = game_name_and_platform.split()
                platform = splitter[len(splitter) - 1]
                platform = platform.strip('()')
                splitter = splitter[:-1]
                game_name = ' '.join(splitter)
                game_name = game_name.replace("'", "")
                # pull Release Date Text
                date_str = element.find_all('span', {'class': 'data'})[1].text
                release_date = datetime.strptime(date_str, '%b %d, %Y')
                # pull User Score
                user_score_str = element.find_all('span', {'class': 'data'})[0].text
                if db_ops.safe_cast(user_score_str, float) is None:
                    user_score = None
                else:
                    user_score = float(user_score_str)

                # pull Critic Score
                critic_score_str = element.find_all('div', {'class': 'metascore_w'})[0].text
                critic_score = int(critic_score_str)
                # generate dataframe for input into database
                df = pd.DataFrame(
                    [(game_name, release_date, platform, user_score, critic_score)],
                    columns=col_names)
                # if the game isn't already loaded into the database load it
                score_id = db_ops.check_game_loaded(game_name, release_date)
                if score_id is None:
                    db_ops.load_data(df)
                    df.drop(df.index[0])
                # otherwise update the entry with a new score
                else:
                    db_ops.update_data(df, score_id)
                    df.drop(df.index[0])

        # if there are multiple page elements, iterate over every page
        else:
            # retrieve the number of pages
            num_pages = int(page_soup.find_all('a', {'class': 'page_num'})[page_num_tags - 1].text)

            # iterates over every page
            for i in range(0, num_pages):
                url = "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?sort=desc&year_selected=" + \
                  str(year) + "&page=" + str(i)

                # if it hangs up, keep trying until success
                while True:
                    try:
                        driver.get(url)
                    except:
                        continue
                    else:
                        break
                page_soup = soup(driver.page_source, "html.parser")
                elements = page_soup.find_all('li', {'class': re.compile('product game_product*')})
                for element in elements:
                    # GameName and Platform
                    game_name_and_platform = element.div.div.a.text
                    splitter = game_name_and_platform.split()
                    platform = splitter[len(splitter) - 1]
                    platform = platform.strip('()')
                    splitter = splitter[:-1]
                    # adds spaces in between text
                    game_name = ' '.join(splitter)

                    # removes all apostrophes. Had issue with entering data with apostrophes in sql. Could not figure
                    # out how to escape it

                    game_name = game_name.replace("'", "")

                    # Retrieves Release Date Text
                    date_str = element.find_all('span', {'class': 'data'})[1].text
                    release_date = datetime.strptime(date_str, '%b %d, %Y')
                    # pull User Score
                    user_score_str = element.find_all('span', {'class': 'data'})[0].text
                    if db_ops.safe_cast(user_score_str, float) is None:
                        user_score = None
                    else:
                        user_score = float(user_score_str)

                    # pull Critic Score
                    critic_score_str = element.find_all('div', {'class': 'metascore_w'})[0].text
                    critic_score = int(critic_score_str)
                    df = pd.DataFrame(
                        [(game_name, release_date, platform, user_score, critic_score)],
                        columns=col_names)
                    score_id = db_ops.check_game_loaded(game_name, release_date)
                    if score_id is None:
                        db_ops.load_data(df)
                        df.drop(df.index[0])
                    else:
                        db_ops.update_data(df, score_id)
                        df.drop(df.index[0])
    driver.close()

if __name__ == '__main__':
    main()


