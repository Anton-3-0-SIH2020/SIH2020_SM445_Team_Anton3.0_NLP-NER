import sqlite3
import requests
import bs4
import csv
from CAGen import generate_corpus, generate_fake_ca


# Initializing the database
def initializeDb():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    create_table = 'CREATE TABLE IF NOT EXISTS news (headline text,content text,link text,category text)'
    c.execute(create_table)
    conn.commit()
    conn.close()

# Adding item in db


def addItemInDb(headline, content, link, category):
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    add_item = 'INSERT INTO news VALUES (?,?,?,?)'
    c.execute(add_item, (headline, content, link, category))
    conn.commit()
    conn.close()

# Scraper for Money Control


def scrapeNews(pageNumber):
    url = f'https://www.moneycontrol.com/news/tags/corporate-action.html/page-{pageNumber}/'
    ist_of_li = []
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='lxml')
    page = soup.find('ul', {'id': 'cagetory'})
    list_of_li = page.find_all('li', {'class': 'clearfix'})
    for li in list_of_li:
        addItemInDb(li.find_all('h2')[0].text, li.find_all(
            'p')[0].text, li.find_all('a')[0]['href'], 'ca')
    print(f'Done acraping and storing page{pageNumber}')

# Scraper for non ca


def scrapeNonCa(pageNumber):
    url = f'https://www.moneycontrol.com/news/business/page-{pageNumber}/'
    ist_of_li = []
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='lxml')
    page = soup.find('ul', {'id': 'cagetory'})
    list_of_li = page.find_all('li', {'class': 'clearfix'})
    for li in list_of_li:
        addItemInDb(li.find_all('h2')[0].text, li.find_all('p')[
                    0].text, li.find_all('a')[0]['href'], 'notca')
    print(f'Done acraping and storing page{pageNumber}')

# Creating CSV from the database


def writeDataInCsv():
    with open('news.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "News"])
        conn = sqlite3.connect('news.db')
        c = conn.cursor()
        readData = 'SELECT * FROM news'
        c.execute(readData)
        for row in c:
            writer.writerow([row[3], row[1]])


if __name__ == "__main__":
    initializeDb()
    generate_corpus.generate_corpus_text()
    generate_fake_ca.generate_fake_ca()
    for i in range(1, 3):
        scrapeNonCa(i)
    print('DONE')
    writeDataInCsv()
