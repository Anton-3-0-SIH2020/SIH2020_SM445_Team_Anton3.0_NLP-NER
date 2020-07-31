from NewsScraper import Money_Control_Scraper
import sqlite3
import csv



# Initializing the database
def initializeDb():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    create_table = 'CREATE TABLE IF NOT EXISTS news (headline text,content text,link text,category text)'
    c.execute(create_table)
    conn.commit()
    conn.close()

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

def createDbOfCaForNer():
    conn=sqlite3.connect('news.db')
    c=conn.cursor()
    c1=conn.cursor()

    create_table='CREATE TABLE IF NOT EXISTS ca_news (content text,category text,purpose text)'
    c.execute(create_table)

    c.execute('SELECT * FROM news WHERE category="ca"')

    add_item_to_table="INSERT INTO ca_news VALUES(?,?,?)"
    for row in c:
        c1.execute(add_item_to_table,(row[1],'null','null'))

    conn.commit()
    conn.close()

if __name__=="__main__":
    # initializeDb()
    # moneyControlScraper=Money_Control_Scraper.MoneyControlScraper()
    # moneyControlScraper.scrapeNews()
    # writeDataInCsv()

    createDbOfCaForNer()