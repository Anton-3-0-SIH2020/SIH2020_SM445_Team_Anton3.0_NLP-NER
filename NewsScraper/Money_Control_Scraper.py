import requests
import bs4
import sqlite3


class MoneyControlScraper:
    # Adding item in db
    def addItemInDb(self,headline, content, link, category):
        conn = sqlite3.connect('./news.db')
        c = conn.cursor()
        add_item = 'INSERT INTO news VALUES (?,?,?,?)'
        c.execute(add_item, (headline, content, link, category))
        conn.commit()
        conn.close()

    #Scraper for money control
    def scrape(self,pageNumber):
        url = f'https://www.moneycontrol.com/news/tags/corporate-action.html/page-{pageNumber}/'
        ist_of_li = []
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features='lxml')
        page = soup.find('ul', {'id': 'cagetory'})
        list_of_li = page.find_all('li', {'class': 'clearfix'})
        for li in list_of_li:
            self.addItemInDb(li.find_all('h2')[0].text, li.find_all(
                'p')[0].text, li.find_all('a')[0]['href'], 'NONE')
        print(f'Done acraping and storing page{pageNumber}')


    # Scraper for non ca
    def scrapeNonCa(self,pageNumber):
        url = f'https://www.moneycontrol.com/news/business/page-{pageNumber}/'
        ist_of_li = []
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features='lxml')
        page = soup.find('ul', {'id': 'cagetory'})
        list_of_li = page.find_all('li', {'class': 'clearfix'})
        for li in list_of_li:
            self.addItemInDb(li.find_all('h2')[0].text, li.find_all('p')[
                        0].text, li.find_all('a')[0]['href'], 'notca')
        print(f'Done acraping and storing page{pageNumber}')

    def scrapeNews(self):
        for i in range(20,30):
            self.scrapeNonCa(i)
        print('DONE')