import sqlite3
import requests,bs4


#Initializing the database
def initializeDb():
    conn=sqlite3.connect('news.db')
    c=conn.cursor()
    create_table='CREATE TABLE IF NOT EXISTS news (headline text,content text,link text,category text)'
    c.execute(create_table)
    conn.commit()
    conn.close()

#Adding item in db
def addItemInDb(headline,content,link,category):
    conn=sqlite3.connect('news.db')
    c=conn.cursor()
    add_item='INSERT INTO news VALUES (?,?,?,?)'
    c.execute(add_item,(headline,content,link,category))
    conn.commit()
    conn.close()


def scrapeNews(pageNumber):
    url=f'https://www.moneycontrol.com/news/tags/corporate-action.html/page-{pageNumber}/'
    ist_of_li=[]
    res=requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text,features='lxml')
    page=soup.find('ul',{'id':'cagetory'})
    list_of_li=page.find_all('li',{'class':'clearfix'})
    for li in list_of_li:
        addItemInDb(li.find_all('h2')[0].text,li.find_all('p')[0].text,li.find_all('a')[0]['href'],'None')
    print(f'Done acraping and storing page{pageNumber}')
    

if __name__ == "__main__":
    initializeDb()
    for i in range(1,6):
        scrapeNews(i)
    print('DONE')

