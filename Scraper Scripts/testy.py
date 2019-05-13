from bs4 import BeautifulSoup as soup
from selenium import webdriver

chrome_path = r"C:\Users\Kevin\Desktop\scraper_stuff\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
url = "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?sort=desc&year_selected=1995"
driver.get(url)
page_soup = soup(driver.page_source, "html.parser")
num_pages = len(page_soup.find_all('li', {'class': 'page'}))
print(num_pages)